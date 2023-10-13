# Login-Authentication-System
Implemented a login authentication System using Flask,flask wtfforms and postgresql

Here are the steps to run the project

### Step 1

#### Create a Enviornment Variable (Create Enviornment Variable Using Conda and venv here is the example using Conda)
python version = 3.10.13

conda create -n yourenvname python=x.x

#### Activate Variable Using command

conda activate yourenvname

### Step 2

#### Install the required libraries

pip install -r requirements.txt

#### Step 3 

In config.json on first run make sure to make CREATE_TABLES='True' and DATABASE as the link to your DATABASE as mentioned in below image here 1234 is password
and Job is Database name make sure to change the Database name and password according to you

![config json - Job Portal - Visual Studio Code 13-10-2023 23_07_35](https://github.com/Abhishek21-ai/Login-Authentication-System/assets/68462503/a71d053e-3a92-4913-b92e-1d4ed3f524d7)



### Step 4

Run the Application using terminal using <b>python regauthv1.py</b>
