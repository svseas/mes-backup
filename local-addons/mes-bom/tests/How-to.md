1. Write tests in the 'test' folder
2. Remember to include the test script in __init__.py
3. Run the test with the following command: 

```bash
sudo docker exec -it {CONTAINER NAME} odoo --test-enable -d {DATABASE NAME} -i {MODULE NAME} --no-http --stop-after-init
```

For example, for the tests run on mes-bom module, use this command: 

```bash
sudo docker exec -it web-odoo-mes odoo --test-enable -d postgres -i mes-bom --no-http --stop-after-init

```