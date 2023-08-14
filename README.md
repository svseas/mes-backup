# Production Docs
## All services
- odoo 16 - Change version in docker-compose if you want. Example: odoo:14
- postgres 13
- pgadmin4 - Manage your postgres odoo database
- nginx - proxy server with config/odoo-nginx.conf
- debug docker  odoo
## How to deploy docker odoo production?
``` bash
docker-compose up -d
```
- Tunr off services
``` bash
docker-compose down 
```
- Turn off and delete all data
```bash
docker-compose down -v
```
## Docker odoo python container
``` bash
docker exec -it web-odoo bash -c "odoo shell -d odoo"
```
## How to include your module in odoo docker for production 
Simply put the folder of your local add-ons into the "local-addons" folder

## Odoo container Bash
Connect Postgres in docker 
```
docker exec -it web-odoo bash
# psql in container
psql -U odoo odoo

```
## pgadmin4 - Manage your odoo database in browser
connect pgadmin4 - port 5433 **localhost:5433**
**Create new server** \
Name your server then modify in **Connection** tab \
hostname/address : db \
username: odoo \
password: odoo \

## MES Project Coding Conventions


1. **Use Meaningful Class and Field Names:**
   Choose descriptive names for your classes and fields. Names should accurately reflect the purpose and functionality of the entities they represent.

2. **Keep Indentation Consistent (4 Spaces):**
   Use 4 spaces for indentation to improve code readability and maintain a clear structure.

3. **Add Docstrings to Classes and Methods:**
   Document your classes, methods, and functions with clear docstrings. Explain their purpose, inputs, outputs, and usage.

4. **Use Underscore Naming Convention for Method Names:**
   Follow the underscore naming convention (`_compute_child_inputs`, `_get_child_process_machines`, etc.) for more readable method names.

5. **Separate Sections with Clear Comments:**
   Use comments to group related fields, methods, and logical sections together. Clear comments enhance code navigation.

6. **Follow PEP8 Guidelines for Import Order:**
   Import modules in the recommended order: standard library modules, third-party library modules, and local project modules.

7. **Add Comments to Describe Complex Calculations or Logic:**
   Explain complex calculations or logic in methods with comments to help other developers understand the code.

By adhering to these conventions, you ensure that your Odoo project's code is readable, understandable, and maintainable.

# Gitflow Convention for MES Project

1. **Branch Naming:**
   - `main`: Represents the production-ready codebase.
   - `feature/feature-name`: Used for developing new features.
   - `bugfix/issue-number`: For fixing bugs or issues.
   - `hotfix/issue-number`: For urgent fixes on the production codebase.
   - `release/version-number`: For preparing a new release.
   
2. **Feature Development Workflow:**
   - Create a new branch from `main` named `feature/feature-name`.
   - Develop the feature in this branch.
   - Regularly commit and push changes to the remote repository.
   - Once the feature is complete, create a pull request to merge it into `main`.

3. **Bugfix Workflow:**
   - Create a new branch from `main` named `bugfix/issue-number`.
   - Fix the bug in this branch.
   - Regularly commit and push changes to the remote repository.
   - Once the bugfix is complete, create a pull request to merge it into `main`.

4. **Hotfix Workflow:**
   - Create a new branch from `main` named `hotfix/issue-number`.
   - Fix the urgent issue in this branch.
   - Regularly commit and push changes to the remote repository.
   - Once the hotfix is complete, create a pull request to merge it into `main`.

5. **Release Workflow:**
   - Create a new branch from `main` named `release/version-number`.
   - Perform final testing and bugfixes on this branch.
   - Once the release is ready, merge it into both `main` and `develop` branches.
   - Tag the release with the version number.

6. **Merging and Pull Requests:**
   - Use pull requests for all merges into `main`, `develop`, and other long-lived branches.
   - Require code reviews for all pull requests.
   - Avoid direct pushes to `main` and `develop` to maintain code quality.

7. **Keep the Repository Clean:**
   - Regularly delete merged feature and bugfix branches to keep the repository clean.
   - Use `git fetch --prune` to remove remote branches that have been deleted.

By following the Gitflow convention, you establish a structured workflow that promotes collaboration, code quality, and a consistent release process.


# Deployment Convention with CI/CD for MES Project

## Continuous Integration and Continuous Deployment (CI/CD)

1. **Version Control System:**
   - Use Git for version control and host the repository on a platform like GitHub.

2. **Codebase Management:**
   - Maintain a clear and structured directory hierarchy for the project's source code.

3. **Branching Strategy:**
   - Follow the Gitflow branching convention for managing different types of branches.

4. **Automated Testing:**
   - Implement automated testing for various aspects of the application, including unit, integration, and end-to-end tests.

5. **Continuous Integration (CI):**
   - Set up CI pipelines using platforms like GitHub Actions, GitLab CI/CD, or Jenkins.
   - Configure CI pipelines to run automated tests whenever changes are pushed to relevant branches.

6. **Code Quality Checks:**
   - Include linting and static code analysis tools in the CI pipeline to maintain code quality standards.

7. **Dockerization:**
   - Dockerize the application to encapsulate its dependencies and ensure consistency across environments.

8. **Container Registry:**
   - Use a container registry (e.g., Docker Hub, GitHub Container Registry) to store Docker images.

9. **Continuous Deployment (CD):**
   - Implement a CD pipeline to automate the deployment process.
   - Use deployment tools like Kubernetes, Docker Swarm, or cloud services (e.g., AWS ECS, Google Kubernetes Engine) for orchestration.

10. **Environment Setup:**
    - Maintain separate environments (e.g., development, staging, production) to ensure proper testing and deployment.

11. **Infrastructure as Code (IaC):**
    - Define your infrastructure using IaC tools like Terraform or CloudFormation to ensure reproducibility and consistency.

12. **Automated Deployment:**
    - Configure the CD pipeline to deploy the application to different environments based on the branch being pushed.

13. **Rollbacks and Monitoring:**
    - Implement a strategy for rolling back deployments in case of issues.
    - Set up monitoring tools (e.g., Prometheus, Grafana) to monitor application performance.

14. **Secrets Management:**
    - Use a secrets management tool (e.g., HashiCorp Vault, AWS Secrets Manager) to handle sensitive information.

15. **Release Notes and Documentation:**
    - Maintain release notes and update documentation with each deployment.

16. **Post-Deployment Tasks:**
    - Automate post-deployment tasks like database migrations and cache clearance.

By following this CI/CD convention, you ensure a streamlined and automated process for building, testing, and deploying your MES project while maintaining code quality, consistency, and reliability across different environments.


# Odoo Repository Pattern Best Practices for MES Project

1. **Modular Structure:**
   - Organize your Odoo project into separate modules representing different components or features of the MES system.

2. **Module Naming Convention:**
   - Use meaningful and consistent names for modules, reflecting their purpose.
   - Follow a naming convention like `mes_<module_name>` for module directories.

3. **Dependencies Management:**
   - Declare module dependencies using the `depends` attribute in the module's manifest file (`__manifest__.py`).
   - Avoid circular dependencies between modules.

4. **Functional Separation:**
   - Divide functionality into discrete modules based on business logic (e.g., manufacturing, inventory, sales).
   - This separation enhances maintainability and reusability.

5. **Custom Add-ons vs. Third-Party Add-ons:**
   - Use custom add-ons for project-specific requirements.
   - Utilize third-party add-ons (from the Odoo App Store) for generic functionalities whenever possible.

6. **Clear Module Descriptions:**
   - Provide clear and informative descriptions in the module's manifest file.
   - Explain the purpose, features, and usage of the module.

7. **Logical Directory Structure:**
   - Follow a consistent directory structure within each module.
   - Organize subdirectories for views, models, security rules, static files, and other components.

8. **Models and Views:**
   - Separate models, views, and other components into their respective directories.
   - Use meaningful model and view names to improve code readability.

9. **Security Rules:**
   - Define security rules for models using XML files within the module.
   - Implement proper access controls for different user roles.

10. **Static Assets:**
    - Store static assets (CSS, JavaScript, images) in the module's static directory.
    - Organize assets by subdirectories if necessary.

11. **Localization:**
    - If your MES system targets different regions, handle localization within dedicated modules.
    - Localize field labels, views, and reports as needed.

12. **Documentation:**
    - Include README files within each module's directory to provide an overview of the module and its usage.
    - Document any special configurations or setup steps.

13. **Version Control:**
    - Use a version control system (e.g., Git) to manage your Odoo project's source code.
    - Commit frequently and use meaningful commit messages.

14. **Code Quality:**
    - Follow coding standards and best practices for Python and Odoo development.
    - Use proper indentation, comments, and variable naming.

15. **Testing:**
    - Implement unit tests for critical components of your modules.
    - Use the Odoo testing framework to ensure code reliability.

16. **Continuous Integration:**
    - Set up a continuous integration pipeline for automated testing and quality checks.

17. **Reusability:**
    - Strive for reusability by creating generic modules that can be easily adapted for similar projects.

18. **Upgrade Considerations:**
    - Keep track of changes in Odoo versions and adapt your modules to new APIs and features.

19. **Versioning:**
    - Use version numbers for your modules to indicate changes and updates.

20. **Code Review:**
    - Conduct code reviews within your development team to ensure code quality and adherence to conventions.

By following these Odoo repository best practices, you'll create a structured, modular, and maintainable project architecture for your MES system. This approach enhances collaboration, scalability, and code quality throughout the development lifecycle.
