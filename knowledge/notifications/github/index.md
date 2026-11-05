# GitHub notifications

* [What makes GitHub notify a person](github-notification-triggers.md) - GitHub notifies a person when they take part in a thread, are mentioned, assigned or asked to review, or watch the repository; everything else, including board changes, reaches nobody
* [GitHub watching, delivery and the inbox](github-watching-and-delivery.md) - How a person chooses which repositories reach them (watch levels, Custom), and where notifications land (web inbox, email, GitHub Mobile push with working hours)
* [GitHub events a notifier can listen to](github-events-for-a-notifier.md) - Webhooks, Actions triggers and the Slack or Teams apps carry GitHub events to other channels; the notifications API itself needs a classic personal token, so an App cannot read anyone's inbox
* [What GitHub never notifies](github-notification-gaps.md) - Board changes, your own actions, mentions added by edit and anything below a phone's normal notification level never reach a person through GitHub; a kit that relies on GitHub alone must design around these gaps
