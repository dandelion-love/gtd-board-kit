# Board model

* [Labels are signals; Status follows](labels-are-signals.md) - Agents set labels, a bridge moves the card
* [Agent sign-in](agent-sign-in.md) - Device-code join a person approves, a 24-hour token with a single-use refresh, revoked means join again
* [Claims and leases](claims-and-leases.md) - One holder per item, recorded by the server, for a limited time
* [Queue and ETA](queue-and-eta.md) - Card order is the queue, a date field is the ETA, a person's edit wins
* [Report vocabulary](report-vocabulary.md) - Six report states and the question for a person
* [Server version and levels](server-version.md) - The server declares its spec version and honest levels; agents run only skills whose level is claimed
* [Where evidence goes](evidence-places.md) - The PR's evidence table is the gate; issue artifacts keep plans and evidence on the issue; sub-issues are never evidence
* [Board fields and who writes them](board-fields.md) - Each standard field has a writer and a moment; a card waiting on a person names the gate and the ask
* [Grants that widen rule 9](grants.md) - A merged, named BOARD.local grant lets an agent merge a PR whose every file it lists, or edit a named workflow
* [Typed links between items](typed-links.md) - A fixed set of link kinds; only depends-on is a native blocked-by, the rest are Related lines on both ends, and one fold feeds the issues and the OKF graph
