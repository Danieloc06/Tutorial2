# Short Toolchain Critque
## What Worked

### API (Movie API)
The movie API was straightforward to integrate and get up and running quickly and was also something all members of the group actually had an interest in. 

### GitHub
GitHub was central to our workflow. Pull requests and GitHub Actions for CI/CD all worked well together. We did have problems at the start with pull requests and trying to sort out different branches however we got more comfortable working with it after a while.

### Docker 
When the Docker file was configured correctly from the advice of the tutors of next steps, it became reliable to operate.

### Supabase
Supabase worked well. Free tier was sufficient for development and the dashboard made it easy to inspect data.

## What we would change
### Switch to Railway
In future projects we would use Railway instead of Render. However, We decided to go with the cheaper options as students.

### Earlier learning of GitHub
Getting more comfortable on GitHub earlier would have helped with less issues for the projects.

## Risks and Mitigations
### Risk 1 - Cloud Platform Billing Costs
**Risk**: Cloud Platforms like Supabase require a credit card on file and will begin charging once the free tiers limits are exceeded. This is a real risk in a project with unpredictable usage as costs can escalate quickly without warning.

#### Mitigations 
- Set a spending cap on the Supabase account to prevent unexpected charges.
- Implement a rate limit on the application so users can only make a set numbers of requests per day.


### Risk 2 - API Downtime
**Risk**: If external API goes down the application loses a core feature and could break entirely which would break the project.

#### Mitigations:
- Monitor the API status and have a backup API identified in advance. 
