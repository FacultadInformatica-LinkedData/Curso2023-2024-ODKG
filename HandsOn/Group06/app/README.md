# PedMad

This project involves setting up Apache Fuseki Server and downloading a Node.js React application from Dropbox.

## Apache Fuseki Server Installation

1. **Download Apache Fuseki Server:**

 Visit the [Fuseki download page](https://jena.apache.org/download/index.cgi) and download the latest version of Apache Fuseki Server. You can use the following command to download it:

 ```bash
   wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.10.0.zip
 ```

2. **Extract the Archive:**

	Extract the downloaded archive using the following command:

 ``` 
 tar -zxvf apache-jena-fuseki-4.10.0.zip

 ```

3. **Navigate to the Fuseki Directory:**

  ``` 
cd apache-jena-fuseki-4.10.0.zip

 ```

4. **Start Fuseki Server:**

	Start the Fuseki server using the following command:
  ``` 
./fuseki-server --update --mem /ds

 ```

 5. **Access Fuseki Server:**

	Open your browser and navigate to http://localhost:3030 to access the Fuseki Server web interface.






## Node.js React Application Download



1. **Download the React Application:**

Download the Node.js React application RAR file from Dropbox using the following command:
  ``` 
wget https://www.dropbox.com/scl/fi/bf2eu8ksk5ommhagthk17/PedMad.rar?rlkey=j2sq17pjtyy33zrvvmhzwqu5z&dl=0 -O app.rar

 ```


2. **Download the React Application:**

Extract the downloaded RAR file using the following command:

	Start the Fuseki server using the following command:
  ``` 
wget https://www.dropbox.com/scl/fi/bf2eu8ksk5ommhagthk17/PedMad.rar?rlkey=j2sq17pjtyy33zrvvmhzwqu5z&dl=0 -O app.rar

 ```

3. **Install Dependencies:**

Navigate to the extracted directory and install the Node.js application dependencies:

  ``` 
cd pedmad
npm install
 ```

4. **Run the Application:**

Start the Node.js React application:

  ``` 
npm start

 ```

The application should now be accessible at http://localhost:3000.

## Additional Notes                
Make sure you have the necessary software (e.g., Node.js, npm) installed on your system before running the React application.
Customize the Fuseki server configuration and the Node.js React application setup based on your project requirements.
