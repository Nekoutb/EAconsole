# EA Console Integration Checklist

This checklist tracks the production integrations for `console.cm-ea.com`. Credentials must be stored on the server as protected environment variables and must never be committed to GitHub or pasted into application JavaScript.

## 0. Security foundation

- [ ] Add IT-team authentication
- [ ] Create protected server-side environment file
- [ ] Add application backend/API proxy
- [ ] Add database for health history, risks, maintenance, and renewals
- [ ] Configure role-based access: Administrator, Operator, Viewer
- [ ] Configure audit logs
- [ ] Configure backup and restore procedure

Information needed:

- IT team members' names and work email addresses
- Preferred login method: email/password, Google Workspace, or Microsoft 365
- Initial administrator email
- Required session duration and MFA policy

## 1. Vultr — server monitoring

- [ ] Retrieve server inventory
- [ ] Monitor instance status, CPU, memory, disk, bandwidth, and uptime
- [ ] Track operating system and region
- [ ] Schedule periodic server health tests
- [ ] Add server-down and resource-threshold alerts
- [ ] Record backup and snapshot state

Information needed:

- Read-only Vultr API key
- Vultr account or organization name
- Expected server list and friendly names
- CPU, memory, disk, and downtime alert thresholds
- Health-check frequency

## 2. Cloudflare — DNS and website edge health

- [ ] Retrieve zones and DNS records
- [ ] Track proxy status and DNS changes
- [ ] Monitor SSL mode and certificate state
- [ ] Monitor Cloudflare incidents and zone analytics
- [ ] Flag unexpected DNS changes

Information needed:

- Restricted Cloudflare API token with Zone Read, DNS Read, Analytics Read, and SSL/TLS Read permissions
- Cloudflare account ID
- Zones to include, starting with `cm-ea.com`
- Approved DNS-change notification recipients

## 3. Website monitoring

- [ ] Confirm complete website inventory
- [ ] Configure HTTP/HTTPS ping checks
- [ ] Measure latency and uptime
- [ ] Validate expected status code and page content
- [ ] Monitor SSL expiry
- [ ] Store check history and incident timelines
- [ ] Configure retries before raising incidents

Information needed:

- Website and API endpoint list
- Expected status code for each endpoint
- Optional text expected on each page
- Check interval, recommended: 5 minutes
- Failure retries, recommended: 3
- Alert recipients and channels

## 4. BitNinja — security monitoring

- [ ] Retrieve protected-server inventory
- [ ] Display security incidents and blocked attacks
- [ ] Track malware and vulnerability status
- [ ] Display WAF and IP reputation events
- [ ] Create high-severity security alerts

Information needed:

- BitNinja API access or API documentation for the account
- Protected server list
- Severity levels that require immediate escalation
- Security incident owner

## 5. Hostinger — domains and expiry

- [ ] Import registered domain inventory
- [ ] Track registration and expiry dates
- [ ] Track auto-renewal state
- [ ] Create 90-, 60-, 30-, 14-, and 7-day renewal reminders
- [ ] Record renewal cost and responsible owner

Information needed:

- Hostinger API access, if available for the account, or exported domain list
- Domain name, expiry date, auto-renewal state, and annual cost
- Billing currency
- Domain owner/responsible person

## 6. Anthropic Claude — API and subscription

- [ ] Track Claude API usage by website/project
- [ ] Display token usage and estimated cost
- [ ] Track monthly budget and threshold alerts
- [ ] Track paid subscription renewal
- [ ] Separate API billing from Claude subscription billing

Information needed:

- Anthropic Admin API key with usage/cost reporting access, not an inference key
- Anthropic organization ID
- Project/workspace mapping to each website
- Monthly API budget and warning thresholds
- Claude subscription plan, price, billing cycle, and renewal date

## 7. OpenAI / Codex subscription

- [ ] Track subscription plan and renewal date
- [ ] Record monthly cost and assigned users
- [ ] Track OpenAI API usage separately if used later
- [ ] Create renewal and budget reminders

Information needed:

- Codex/ChatGPT plan name
- Monthly or annual cost and currency
- Renewal/billing date
- Number of paid seats and assigned users
- OpenAI organization/project details only if API usage will be monitored

## 8. MailerSend

- [ ] Track subscription plan, cost, and renewal date
- [ ] Monitor monthly email quota and usage
- [ ] Monitor delivery, bounce, complaint, and rejection rates
- [ ] Track domain verification status
- [ ] Alert on quota and deliverability thresholds

Information needed:

- Restricted MailerSend API token
- Plan name, price, currency, and billing date
- Monthly quota
- Sending domains
- Bounce, complaint, and quota alert thresholds

## 9. Maintenance planning

- [ ] Create maintenance calendar
- [ ] Assign maintenance owner and approver
- [ ] Track planned start/end time and affected services
- [ ] Record pre-checks, rollback plan, and post-checks
- [ ] Publish maintenance status in the console

Information needed:

- Standard maintenance window and timezone
- Owners and approvers
- Notification lead time
- Required maintenance checklist

## 10. Risk register

- [ ] Create risk submission form
- [ ] Define severity and likelihood scales
- [ ] Assign owners and due dates
- [ ] Track mitigation actions and evidence
- [ ] Escalate overdue high risks

Information needed:

- Risk categories
- Severity and likelihood definitions
- Risk owners and escalation recipients
- Review frequency

## 11. Alerts and reports

- [ ] Configure email alerts
- [ ] Add optional Teams or Slack alerts
- [ ] Produce daily operational summary
- [ ] Produce weekly uptime and risk report
- [ ] Produce monthly subscription cost and renewal report

Information needed:

- Alert email recipients
- Preferred messaging channel
- Escalation schedule
- Report recipients and delivery times

## Recommended implementation order

1. Security foundation and IT-team login
2. Website monitoring
3. Vultr
4. Cloudflare
5. BitNinja
6. Hostinger domains
7. MailerSend
8. Anthropic Claude
9. OpenAI/Codex subscription
10. Maintenance, risk, alerts, and reports
