# Machine fit

A machine says what it has, an item says what it needs ([item needs](tools.md#finding-work)),
and `list_next_actions` offers a machine only the items it can finish. Everything here is
optional and additive: a server that does not offer it, and a call that does not use it,
behave as before.

## The machine card

A registered resource MAY carry a **card**: what the machine offers. Every field is
required when a card is set, so a card is never half known:

| Field | Type | Meaning |
| --- | --- | --- |
| `graphics_gb` | number, 0 or more | Graphics memory in GB (0 for none) |
| `free_storage_gb` | number, 0 or more | Free storage in GB |
| `tools` | list of tool names | Installed tools: lowercase letters, digits, `.`, `_`, `-`, at most 40 characters each, read as lowercase, repeats listed once, at most 50 |
| `speed_minutes` | number, above 0 | Minutes **this machine takes for the fixed reference job** |

The reference job is a fixed unit of work whose definition the operator publishes with the
server; the figure is a measurement, not an estimate of any one item. It is comparable with
an item's `longest_run_minutes` because both are minutes.

A card has **generic fields only**. A field outside the table is refused and named, so a
card cannot carry a credential, a hostname or a path. A server refuses a card whose field is
missing, not a number (a boolean is not a number), out of range or unknown, and the refusal
names every such field, in the table's order; nothing is stored. A card is set when the
resource is registered and replaced as a whole when it is updated, by the resource's owner
or an administrator, and is returned by the resource read tools. An update that leaves the
card out keeps the stored one. Check MF1 holds a server's validation to
[machine_fit_cases.json](../conformance/machine_fit_cases.json); the reference is
[machine_fit.py](../conformance/machine_fit.py).

## Fit

`list_next_actions` takes an optional `resource` (a registered resource id). Without it the
call is exactly what it was. With it:

- An **unknown** resource, a resource with **no card**, and a call made without the right to
  read resources are refused, and nothing is offered.
- An item that **runs anywhere** (nothing declared; a Size default is not a declared need) is
  offered to every machine.
- Otherwise the item fits when the card has at least the item's `graphics_gb`, lists every
  one of its `tools`, and `speed_minutes` (times the profile's `fit_speed_factor`, default 1)
  is at most its `longest_run_minutes`. A longest run from the Size default counts once the
  item declares any need. With no longest run, speed is not compared.
- An item that does not fit is **held back**, not offered, and the result lists it under
  `held_back` as `{number, title, reasons}`. A reason reads exactly
  `needs 20 GB graphics, machine has 8 GB`, `needs tool voice, machine does not list it` or
  `longest run 15 minutes, machine needs 45 minutes for the reference job` (numbers print
  without a trailing `.0`). Reasons come in the order graphics, tools, run.
- Fit is decided **before the offer**: an `inferred` `item_claim` is not refused for fit.
  The claim itself does not take a resource.

The rule is not a reservation: it does not choose between machines, order work or hold a
machine. Check MF2 holds a server's rule to the fit cases; MF3 and MF4 are the live checks.
Without `resource` the result is the plain list. With it the result is an object
`{resource, items, held_back}`, where `items` are the rows the plain call would give, so a client
that sends `resource` reads `items`.
