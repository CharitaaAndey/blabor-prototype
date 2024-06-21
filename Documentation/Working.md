### Project Documentation: Automated Message Sending Prototype

#### Overview

This project is designed to automate the process of sending personalized, messages to business owners, encouraging them to register their own domain names. The messages are generated based on the provided data and should be using the appropriate platform for SMS communication.

![Screenshot](./images/Screenshot.png)

I learned to use Mailchimp in my academic project, but I wanted to explore more options. Upon exploring, I found several bulk messaging platforms, which I still need to research and work on. I have divided this project into three phases:

1. **Phase 1: Generating Messages with Respective Domain Names**:
    - This phase involves generating personalized messages for each business owner with a hyperlink to register their domain names. This phase has been completed.

2. **Phase 2: Finding the Right Platform**:
    - This phase is about researching and identifying the right bulk messaging platform, considering pricing and the services they offer. This phase is ongoing.

3. **Phase 3: Google GDPR Analytics**:
    - In this phase, I plan to integrate Google GDPR analytics to generate reports on clients who visited their respective business links and follow them up based on their activity.

I worked on this code with the help of ChatGPT. ChatGPT suggested Twilio for the bulk messaging part, which I integrated into the code. However, for testing, Twilio requires a charge and approval from the clients to receive messages.

#### Basic Structure of the Code

1. **Importing Libraries**:
    - The script imports necessary libraries, including `pandas` for data manipulation, `os` for directory handling, and `twilio` for sending SMS messages.

2. **Twilio Configuration**:
    - The script sets up Twilio configuration with your Account SID, Auth Token, and Twilio phone number to authenticate and send messages.

3. **Loading Data**:
    - The script reads the provided Excel file containing business owner information.

4. **Generating and Sending Messages**:
    - Iterates through each row of the data, generates the personalized message, and sends it via SMS using the Twilio API.

5. **Saving Output**:
    - Ensures the output directory exists and saves the generated messages to a new Excel file for record-keeping.

### Integrating with Twilio

#### What is Twilio?

Twilio is a cloud communications platform that allows you to programmatically send and receive text messages, make and receive phone calls, and perform other communication functions using its web service APIs.

#### Benefits of Integrating with Twilio

1. **Scalability**:
    - Twilio's platform is designed to scale, allowing you to send large volumes of messages without worrying about infrastructure.

2. **Reliability**:
    - Twilio offers reliable delivery with built-in failover and monitoring to ensure your messages are delivered.

3. **Ease of Use**:
    - The Twilio API is straightforward and well-documented, making it easy to integrate with your applications.

4. **Global Reach**:
    - Twilio supports sending messages to phone numbers globally, making it suitable for applications with an international user base.

5. **Tracking and Analytics**:
    - Twilio provides detailed logs and analytics, allowing you to track message delivery and engagement.

### Example of Hyperlink Output

Here's an example of the personalized message that includes the required hyperlink:


Hi John Doe,

🎉 Congratulations on taking the first step towards an even brighter future for Doe's Bakery! 🎉

Imagine your business with its very own domain. It's time to make it official and stand out online! 🌟

Click here to register your custom domain: https://www.secureserver.net/products/domain-registration/find/?domainToCheck=Doe's+Bakery&plid=487856&itc=slp_rstore

Don't miss out on this chance to shine! ✨

Best regards,
Blabor Team
```

