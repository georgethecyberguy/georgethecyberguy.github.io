---
group: lab
title: "Hardening Azure Storage with Terraform"
order: 7
year: 2026
kind: Lab
status: Complete
role: Author
stack:
  - Terraform
  - Azure
  - Azure CLI
  - Bash
summary: A small Infrastructure-as-Code lab provisioning a deny-by-default Azure Storage Account with secure baseline controls — and verifying the posture actually applied.
---

A short, deliberately small Azure + Terraform lab that does something more interesting than spinning up a VM: provision a storage account hardened by default, and *verify* the controls actually took effect. The whole exercise runs in 30-45 minutes in a KodeKloud Azure playground, but it ends up demonstrating a handful of patterns that matter more than the surface activity.

## Why storage, not a VM

Storage misconfiguration is the most common category of public cloud data exposure — the Azure analogue of the perennial S3-bucket-left-open story. A storage account provisioned with permissive defaults is roughly the worst-case footgun in the cloud. Building one *correctly* — denied by default, no public access, TLS 1.2 enforced, HTTPS-only data plane — is small enough to do in one sitting but representative of the kind of judgment that matters in real environments.

## What got built

Three resources, all provisioned through Terraform:

1. A **random string** to suffix the storage account name (account names must be globally unique).
2. A **storage account** with security baked into the configuration, not bolted on after.
3. A **private container** inside it.

The resource group itself was *referenced* via a data source rather than created — more on why below.

## The configuration

The full Terraform lives in three files. The interesting bit is `main.tf`:

```hcl
data "azurerm_resource_group" "lab" {
  name = var.resource_group_name
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
  numeric = true
}

resource "azurerm_storage_account" "lab" {
  name                = "sttflab${random_string.suffix.result}"
  resource_group_name = data.azurerm_resource_group.lab.name
  location            = data.azurerm_resource_group.lab.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  # ---- security controls ----
  https_traffic_only_enabled      = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = true

  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
  }
}

resource "azurerm_storage_container" "private" {
  name                  = "private-data"
  storage_account_id    = azurerm_storage_account.lab.id
  container_access_type = "private"
}
```

Four security controls in the storage account block, each addressing a specific class of cloud risk: TLS downgrade attacks, plaintext data plane traffic, accidental public exposure, and broad public network access. None of them are exotic — they're the baseline posture an auditor would expect to find on any production Azure storage account.

## Verifying the posture

The Terraform code is the *claim*. The Azure CLI is the *proof*:

```bash
az storage account show \
  --name sttflabo9m4v4 \
  --resource-group kml_rg_main-934bb75cbc7d46dd \
  --query "{publicAccess:allowBlobPublicAccess, tls:minimumTlsVersion, httpsOnly:enableHttpsTrafficOnly, defaultAction:networkRuleSet.defaultAction}"
```

The expected output:

```json
{
  "defaultAction": "Deny",
  "httpsOnly": true,
  "publicAccess": false,
  "tls": "TLS1_2"
}
```

Four controls, one query, posture confirmed. This is the pattern that matters more than the provisioning itself: apply, then *verify*. Cloud audits work the same way — the configuration says one thing, but you don't trust it until you query the actual state.

## Negative testing

A deny rule that silently allows traffic is worse than no deny rule at all — it creates false confidence. So the next step was to confirm the network deny actually denies:

```bash
az storage blob list \
  --account-name sttflabo9m4v4 \
  --container-name private-data \
  --auth-mode login
```

Result:

```
The request may be blocked by network rules of storage account.
```

That error is the lab succeeding. The control did exactly what it was configured to do.

## Adapting to the environment

This is the section that turned out to be the most useful part of the lab.

The original plan was to have Terraform create the resource group itself. That's the textbook pattern in every Azure-Terraform tutorial. The first `terraform plan` made it clear that wasn't going to work:

```
Error: Terraform does not have the necessary permissions
to register Resource Providers.
```

Then, after fixing that with `resource_provider_registrations = "none"`:

```
Error: a resource with the ID "/subscriptions/.../resourceGroups/..."
already exists - to be managed via Terraform this resource needs
to be imported into the State.
```

The KodeKloud playground documentation eventually confirmed the constraint plainly: *"The Azure playground does not include the option to create additional resource groups."* Users are handed a pre-existing one and must work within it.

This forced a more enterprise-realistic pattern. In any real organization, a platform team usually owns subscription- and resource-group-level scaffolding, and application teams provision *into* what already exists. The fix was to reference the existing group as a data source instead of a managed resource:

```hcl
data "azurerm_resource_group" "lab" {
  name = var.resource_group_name
}
```

The downstream resources then consume `data.azurerm_resource_group.lab.name` and `.location` in place of the original `azurerm_resource_group.lab` references. The provisioning succeeds; the resource group itself stays read-only from Terraform's perspective; and the configuration now models a more realistic ownership boundary.

When `terraform destroy` runs at the end, it cleans up only what it created — the storage account and container disappear, and the resource group is left untouched, exactly as expected. That's the lifecycle pattern this lab was supposed to demonstrate in the first place, just made more explicit by the constraint.

## Friction worth documenting

A few things broke in instructive ways:

- **`hashicorp` typo in the provider source.** The first `terraform init` failed because the provider source string read `hasicorp/azurerm` (missing `h`). The error message — `provider registry.terraform.io does not have a provider named registry.terraform.io/hasicorp/azurerm` — telegraphs the fix if you read it literally. Lesson: when Terraform says it can't find a provider, check the source string before assuming the registry is down.
- **Resource provider registration permission.** The playground denies user-level resource provider registration. Terraform's default behavior is to try and register on every apply, which fails. The fix is one line in the provider block: `resource_provider_registrations = "none"`. The error message includes the fix verbatim.
- **Cloud Shell session loss.** A frozen terminal during `terraform apply` led to a forced session restart, which lost in-memory editor state and required recreating the `.tf` files. Lesson learned: after using `code .` in Cloud Shell, always `ls` and `cat` to confirm writes actually flushed to disk before running anything that depends on them. The heredoc pattern (`cat > file.tf << 'EOF'`) writes directly through the shell and bypasses that risk entirely.

## What the lab actually demonstrates

Provisioning the storage account is the surface activity. The patterns underneath are what generalize:

- **Secure by default.** Hardening lives in the provisioning code, not as a remediation step afterwards. Anyone reusing this Terraform inherits the controls automatically.
- **Data sources for inherited infrastructure.** The brownfield pattern of consuming pre-existing scaffolding rather than creating it.
- **Apply-then-verify as discipline.** Configuration is a claim; queried state is the proof.
- **Negative testing.** Confirming that what should be blocked actually gets blocked.
- **Clean teardown.** `terraform destroy` removes only what was created, leaving the broader environment intact.

A small lab. Real habits.

## Tear down

```bash
terraform destroy -auto-approve
```

Output:

```
azurerm_storage_container.private: Destruction complete after 1s
azurerm_storage_account.lab: Destruction complete after 2s
random_string.suffix: Destruction complete after 0s

Destroy complete! Resources: 3 destroyed.
```

Three destroyed — the same three that were created. The resource group, owned by the platform, survives.

Exactly the pattern you'd want in production.
