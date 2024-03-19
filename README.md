
# Policy Management App

This is a simple policy management application built with Flask.

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Testing](#testing)
5. [Contributing](#contributing)
6. [License](#license)

## Description
The application allows users to manage policies and rules associated with those policies. It provides functionalities to create, read, update, and delete policies and rules.

## Installation
To install and run the application locally, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/Brylov/policies_network_python.git
    ```

2. Navigate to the project directory:
    ```bash
    cd policy-management-app
    ```

3. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### Starting the Flask App
1. Navigate to the `stage1`, `stage2`, or `stage3` directory based on the desired stage.
2. Run the Flask app using the following command:
    ```bash
    python app.py
    ```
3. The Flask app will start running at `http://127.0.0.1:5000/`.

### Interacting with the App
1. Open your web browser and go to `http://127.0.0.1:5000/`.
2. You can use the provided forms and buttons to perform actions such as creating, reading, updating, and deleting policies and rules.

## Testing
The application includes automated tests to ensure its functionality. To run the tests, follow these steps:

1. Navigate to the `stage1`, `stage2`, or `stage3` directory based on the desired stage.
2. Run the following command to execute the tests:
    ```bash
    pytest -v -s test_stage.py
    ```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please create a pull request or open an issue in the GitHub repository.

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize this README to better suit your project's needs!