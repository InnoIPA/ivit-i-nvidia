# iVINNO-WEB-API

## Workflow
1. Make sure the docker images is built ( ivinno-trt and ivinno-vino )
2. Make sure exit the docker container
3. Prepare virtualenv for web service
    ```bash
    # install pip
    sudo apt-get install python3-pip
    # install virtualenv
    sudo pip3 install virtualenv
    mkdir ~/.virtualenvs
    # install virtualenvwrapper
    sudo pip3 install virtualenvwrapper
    # add the line below to ~/.bashrc
    export WORKON_HOME=~/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    . /usr/local/bin/virtualenvwrapper.sh
    # reload ~/.bashrc
    source ~/.bashrc
    # create a environment and work on it
    mkvirtualenv init-i
    workon init-i
    # install python package
    cd {/path/to/iVINNO-api}
    pip3 install -r requirements.txt
    ```
4. Run iNIT-I server
    ```bash
    # Main web api
    ./run_web_api.sh -n main -b 0.0.0.0:5000
    
    # tensorrt web api
    # run_web_api.sh -n tensorrt -b 0.0.0.0:5001
    
    # openvino web api
    # run_web_api.sh -n openvino -b 0.0.0.0:5000
    ```

5. Run the client: create a new terminal or use other computer
    ```
    git clone https://github.com/InnoIPA/ivinno-web-demo.git
    cd ivinno-web-demo
    unzip static/vendor.zip
    workon init-i
    ./demo.sh -f trt
    ```
6. Open the browser and enter the url
    ```

    ```