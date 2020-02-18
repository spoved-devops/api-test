###API Interaction Demo

####The challenge:
>*Instructions*
>We would like you to demonstrate your understanding of writing code to interact with API’s. To demonstrate this, your goal is to write a program which will pull contents from an API endpoint and write it to a database.
>
>Get the data from the following API endpoint. Its open, no authentication needed. https://api.nanoporetech.com/oracle/v1/requisitions
>Parse the output and insert it into a database of your choice. 
>
>*Solution notes*
>* In the solution please provide clear instructions that will allow us to replicate the solution. 
>* Use a docker container for the DB instance. Just off the shelf image is fine. (MySQL, Postgres)
>* You can use Python to write the code or any language of your choice. You can also use an ORM to interact with the database. (https://orator-orm.com/)
>* Commit often to show work in progress rather than one big push. 
>* The data installed does not have to delivery any particular functionality. 
>
>*Submitting*
>* Put your solution in a public Github or Gitlab repo and send a link. Include a clear README with installation instructions.

####Outline Plan
* Determine data format
  * Curl to the URL
  * Determine fields/type etc.
* Identify target DB type/Docker image
  * Majority common fields -> SQL
  * Varying fields -> NoSQL/DocumentDB
* Script:
  * Extract into data structure
  * Create DB and schema
  * Transform as needed
  * Load into DB
* Look into using an ORM

####Assumptions:
* Python3
* No custom image
* User/pass for DB specified on docker command line is fine
* No need to go as far as Docker Compose to bring up service etc.
* No need to determine field names/types dynamically at run time
* System on which the solution will be replicated has Docker available
* MySQL container can have port published to localhost:3306

####Instructions
Install PIP, setuptools, Orator and a MySQL client for Python3:
~~~
sudo apt install python3-pip
sudo apt install python3-setuptools
sudo pip3 install orator
sudo pip3 install PyMySQL
~~~

Fire up a Docker container running MySQL, creating a DB and setting credentials:
~~~
sudo docker run -d -p 3306:3306 -e MYSQL_DATABASE=apitest -e MYSQL_USER=test-user -e MYSQL_PASSWORD=test-pass mysql/mysql-server --default_authentication_plugin=mysql_native_password
~~~

Clone this repo:
~~~
git clone https://github.com/spoved-devops/api-test.git
~~~

Run loader.py:
~~~
python3 loader.py
~~~

Read/examine data as desired using a local mysql client and credentials as specified on the Docker command line

Once complete, don't forget to clean up the docker container!

####Limitations/Improvements:
* Dynamically determine field types at runtime
* Field lengths are set as either 255 characters or the longest length found for that field in the JSON returned by the API endpoint, whichever is longer
* Fields are treated as either int or string, and don't cater for date/times; we'd need to do some validation/error handling on string formats for the "pub_date" field
* Any field is allowed to be null
* Could use a custom Docker image with the python script embedded
* No exception handling

I rejected the option of using a standard MySQL image and using a bind mount/volume with custom command as it wouldn't just be a case of running the python script - we'd need to get pip, setuptools, orator and a Python MySQL client up and running as well, all from that custom command/script/mount.  For a more self-container/re-usable solution, I'd go for a customer Docker image with the scripts/tools built-in.