# HOW TO RUN TEST IN DOCKER

1. Write tests in the 'tests' folder
2. Remember to include the test script in ```__init__.py```
3. Run the test with the following command: 

```bash
sudo docker exec -it {CONTAINER NAME} odoo --test-enable -d {DATABASE NAME} -u {MODULE NAME} --no-http --stop-after-init
```

For example, for the tests run on mes-bom module, use this command: 

```bash
sudo docker exec -it web-odoo-mes odoo --test-enable -d postgres -u mes-bom --no-http --stop-after-init
```

