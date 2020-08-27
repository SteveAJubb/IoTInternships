# IoTInternships
Summer 2020 University of Sheffield IoT Internships
# Indoor-Air-Quality
# **How to use MQTT to get information from The Things Network using Node Red**

1) Install Node Red - found this video helpful 
	https://www.youtube.com/watch?v=TbXU3PRDN1w
Indoor air quality sensing project

2) To run Node red, open the command window and just type **node-red**

3) After pressing enter a chunk of text is printed in the window, to access Node Red copy and paste the highlighted link to your browser.\
![Command Window](https://user-images.githubusercontent.com/36086687/91428714-6d7d9680-e856-11ea-96ea-a926b4b4a3ed.PNG)

4) The following screen should then appear:\
![Node Red Home](https://user-images.githubusercontent.com/36086687/91430141-c6e5c580-e856-11ea-8c42-64bcc82b4801.PNG)

5) To add an MQTT node scroll down the nodes on the left hand side and click and drag the 'mqtt in' node under 'network' to the main part of the screen.\
![Node Red Nodes](https://user-images.githubusercontent.com/36086687/91430532-f0065600-e856-11ea-9c7e-99683fb988cd.PNG)

6) Double click the MQTT node to edit and click the pencil button next to the 'add a new mqtt-broker' button.\

![Add Broker](https://user-images.githubusercontent.com/36086687/91430497-e381fd80-e856-11ea-8bed-27563bbec024.PNG)

7) Under connection, for devices registered in europe enter 'eu.thethings.network' under server:\
![Server](https://user-images.githubusercontent.com/36086687/91430563-fd234500-e856-11ea-90d8-73ede670dc9d.PNG)

8) Under the security tab, you will need information from The Things Network. Under the 'Application Overview' heading of your device you will need the Application ID which will be the username.\

![Username](https://user-images.githubusercontent.com/36086687/91430367-d533e180-e856-11ea-92a9-b9d604882e11.PNG)

9) You will also need to copy the access key for the the password, by clicking on the clipboard button.\

![Password](https://user-images.githubusercontent.com/36086687/91428131-4757f680-e856-11ea-98ed-b807ecdae38c.PNG)

10) After entering the username and password, click update and enter a name under the node topic and click done.\

11) Then click and drag the debug node to the right of the MQTT node and attach them.\
![Debug](https://user-images.githubusercontent.com/36086687/91441461-27313300-e868-11ea-9026-e3110135cece.PNG)

12) Click deploy and then the debug button to view the incoming messages.\
![Debug Window](https://user-images.githubusercontent.com/36086687/91441900-e7b71680-e868-11ea-94ba-56a2f52b8379.PNG)

