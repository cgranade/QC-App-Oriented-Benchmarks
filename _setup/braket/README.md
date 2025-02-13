# Quantum Computing - Toolkit Information

# Amazon Braket Version

This directory describes the requirements and operational conventions for using Braket as the programming environment for running the prototype benchmark programs contained in the QC-Proto-Benchmarks repository.
In particular, this document explains how to set up the tools needed to run the Braket implementation of these benchmarks.

Note: the instructions contained here describe configuring a Windows environment to run the benchmark programs. Similar procedures will be used in a Linux environment using appropriate syntax of course.

## Configure a Python Environment

The Braket version of the prototype benchmark programs require that you have available Python version 3.6 or later, and have installed the necessary Python packages.

If you have a proper Python environment available, skip this section and go directly the the *'Install Braket'* section below.

If you do not already have Python available, a convenient way to set one up is to download a minimum version of the Anaconda package (called Miniconda). Go to the URL below and follow the instructions to set up the "Miniconda" package.

    https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html

Once you have installed the Miniconda package, from the Windows Start menu launch an Anaconda prompt in which you will run the programs. It is recommended that you create a conda "environment" to hold the specific set of Python packages you will install to run the benchmark programs. Create an environment named "braket" and then "activate" it using the following commands:

    conda create -n braket python=3

    conda activate braket

The conda environment is now ready for you to install the braket package.

## Install Braket

Enter the following commands to install the latest version of Amazon Braket SDK with additional visualization tools.

    pip install boto3

    pip install amazon-braket-sdk

You are now ready to run the benchmark programs.
By default, all benchmark programs are configured to run on a simulator that is provided within the target environment.
Follow the instructions below to run the benchmarks using the built-in Local Quantum Simulator.

To run on any of the quantum hardware devices or the managed simulators provided by Amazon Braket, you must have an Amazon Braket account.
You can go to the following link to create an account or to login to an existing account:

    https://aws.amazon.com/braket/
    
Once you have an account, you will need to set the following environment variables to run a program that accesses Amazon Braket services.
The values for the first two of the variables below can be found in the "Your Security Credentials page of your Braket account.
The region is shown in the dropdown at the top to the right of your name.
The remaining 2 were selected by you during account setup and may be found in your S3 management console.

    AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
    AWS_DEFAULT_REGION = "YOUR_AWS_DEFAULT_REGION"
    AWS_BRAKET_S3_BUCKET = "YOUR_AWS_BRAKET_S3_BUCKET"
    AWS_BRAKET_S3_PREFIX = "YOUR_AWS_BRAKET_S3_PREFIX"

Once these variables are set, you may proceed to execution the benchmark programs in either a Jupyter Notebook or in a command shell window.

## Run the benchmark programs in a Jupyter Notebook

The easiest way to configure and run the Application Benchmark programs is to use a Jupyter Notebook that is provided at the top level of the Proto-Benchmarks repository.
Support for Jupyter notebooks is automatically available with your Anaconda installation.

Frist, prepare the Amazon Braket notebook by copying the delivered 'template' file with the following command:

    copy benchmarks-braket.ipynb.template benchmarks-braket.ipynb
    
To run the Amazon Braket notebook, simply execute the following command to launch the Jupyter Notebooks server.

    jupyter-notebook

This will invoke the Jupyter notebook in a new browser tab.
There you can select the **benchmarks-braket.ipynb** notebook file to open it in a new browser tab.

Once opened, you will see a number of notebook cells.
The first cell is used for configuring various parameters to the benchmark programs and is typically run each time you would like to modify parameters.

The remaining cells contain the benchmark programs, one per cell.
You may run one or all the benchmark programs by simply executing the desired cell(s).
Parameters applied in the first cell apply to the execution of any one of the cells.

Note that in the first section, several lines are commented out by default. 
These lines are used to select and configure execution parameters when running on quantum hardware devices.
Choose the lines to uncomment and modify as desired.

Important Note:
```
The examples shown configure a smaller number of qubits, circuits, and shots for execution on quantum hardware.
This is to avoid accidental execution of large or lengthy quantum circuits on hardware 
that could result in high billing charges.
It is best to begin your exploration with smaller numbers as you become familiar with the available systems.
```

## Run the benchmark programs in an Anaconda command window.

Each of the benchmark programs may be run directly from within a command shell window. 
The code for the each of the application benchmarks is largely self-contained, except for a few references to the folder at top-lvel named **_common**.

For example, in an Anaconda command window, you can enter the following commands to change directory to the Braket Bernstein-Vazirani directory and run the benchmark program:

    cd [your github home directory]\QC-Proto-Benchmarks\bernstein-vazirani\braket
  
    python bv_benchmark.py
    
This will execute the benchmark program, report the benchmark metrics to the console, and invoke a set of bar charts showing the results in visual form.
All other benchmarks follow a similar pattern and structure and are executed in the same way (using the appropriate benchmark pgrogram filename).

Important Note:
```
The application benchmarks are executed from the command line and invoke the main method in the program.
Values of parameters to the programs are hardcoded within the application and default to larger 
values that can run on the Local Simulator with no issue.

To modify the parameters or to switch to execution on quantum hardware, it is necessary to modify
the values of the parameters within the program code (currently).
If you modify the code to execute on quantum hardware, be sure to use smaller values for max_qubits,
max_circuits, and num_shots parameters to avoid incurring high billing charges.
```

## Troubleshooting Tips

In some environments, you may encounter problems running a Jupyter Notebook.

1) In some Windows environments, when running Miniconda, it is necessary to install an additional package (if running a Jupyter notebook results in a Windows "kernel error").
Once the following package is installed, you should be able to successfully start your Jupyter notebook.

    conda install pywin32
    
2) Additionally, after the amazon-braket-sdk package is installed, it may not be recognized within your Jupyter notebook.
Often, executing the following lines will address this problem:

    conda install notebook ipykernel
    ipython kernel install --user

