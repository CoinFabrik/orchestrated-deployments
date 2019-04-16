# Jenkins Tasks

### Setup

Sets up the virtual environment, and compiles the contracts.
**It should be ran once to setup the deployment environment upon jenkins.**
You must scope your credentials in this task. To do that:
- Press the checkbox: "Use secret text(s) or file(s)"
- Bind both your decryption password and your standard keyfile with the names KEYFILE and DECRYPTPASS respectively.

### Upgrade

It runs the upgrade script.
You must scope your credentials in this task. To do that:
- Press the checkbox: "Use secret text(s) or file(s)"
- Bind both your decryption password and your standard keyfile with the names KEYFILE and DECRYPTPASS respectively.

### Test Upgrade

Runs the test and then the upgrade task if it succeed. 
Note that you need to link this job to Upgrade:
- Select at the bottom of the form (Post-Build options)
- Build other projects
- Write down the name of the tasks "Upgrade"