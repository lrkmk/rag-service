# Atlas Security and Compliance

These Terms of Service ('Terms') detail the security and compliance features available to you when you use Atlas API and the ATRIP Flight Deck. Enabling these features will significantly enhance the security of your account and protect your data from unauthorized access.

**These features also allow you to:**

* Manage who has access to your Atlas account at any time;
* Protect it from unauthorized users;
* Set up authentication rules in line with your company’s protocols;
* Monitor and audit all activity, simplifying your compliance process;
* Respond immediately to any incidents.

{% hint style="warning" %}
Only an account administrator can set up and change security settings for your company account.
{% endhint %}

**To enable and set up security features, visit the My Profile page on the ATRIP Flight Deck.**

**1. ACCESS KEYS (AK/SK)**

To access Atlas API, Atlas customers need to setup their access keys (also known as AK/SK, "Access Key" and "Secret Key"). These keys are used for accessing APIs or other services that require secure authentication.

Users must provide these keys when making API calls, and the system uses these keys to verify the user's identity and access privileges. Proper management of these keys is critical for account security, as anyone with access to these keys can access the associated resources.

* Access Key (AK): This is a publicly visible identifier, similar to a user ID, used to identify the sender of a request. It tells the service which user or account is attempting to perform an operation.
* Secret Key (SK): This is a private credential, similar to a password, known only to the user who is authorized to set up the access keys (the account administrator). It is used to verify that the sender of the request has the authority to access the service and to ensure that the request is genuinely initiated by that user.

**All Atlas customers are required to set up access keys to gain access to Atlas API.**

How to set up your Access Keys on the ATRIP Flight Deck:

* To set up or reset your access keys, visit the Company Information\* section of the ‘My Profile’ page on the ATRIP Flight Deck account and follow the instructions on the page.
* You will see a new security key on the screen. Make sure to copy it and store it securely before you complete the setup.
* Once you complete the setup, you won’t be able to see the security key on the ATRIP Flight Deck. It protects your access keys from unauthorized users.
* Once you get a new security key, your technology team needs to reset the keys in your system immediately to complete the process.

{% hint style="warning" %}
Only Account Administrators have access to the Company page on the ATRIP Flight Deck and can issue new access keys. If it's you, please follow the instructions above. If you don’t have access to this function, please contact your account administrator when it’s time to update the keys.
{% endhint %}

**To maintain access to their Atlas account, Atlas customers need to regularly reset access keys.**

* Your access keys are valid for a limited period of time.
* We recommend rotating your access keys every 3 months. However, you can change your renewal cycle according to your company’s protocols. You can choose a renewal cycle: 3 months, 6 months, or 12 months.
* You can have 2 valid AKs at once.
* When your access keys are about to expire, your account administrator will be notified via e-mail\*.
* If access keys are not renewed on time, you will temporarily lose access to Atlas API.
* When you call API with an expired key, you will receive an error code notifying you that your key is not valid. Transactions will stop.
* To restore access to your account, your account administrator needs to visit the ATRIP Flight Deck and reset the keys. The new security key needs to be integrated into API to restore access.
* To avoid disruption in our service, you need to regularly update your keys and reset their expiry date.

{% hint style="info" %}
To ensure you receive all our updates and important information, please add our email address <noreply@atriptech.com> to your trusted contacts list. This will prevent our messages from ending up in your spam folder.
{% endhint %}

**2. SINGLE SIGN-ON (SSO)**

Single Sign-On (SSO) allows your team to access the ATRIP Flight Deck with a single set of credentials – the same set they use to access your own systems.

This feature is particularly useful when you have a large team, and many people need regular access to the ATRIP Flight Deck.

Using Single Sign-On has benefits for all members of the team.

* **Account administrator:** No need to manually add new people to your ATRIP Flight Deck and remember to remove them when they leave your company.
* **Technology team:** Maintain centralized access control to manage and enforce security policies from a single point.
* **Operations and Finance teams:** No need to remember or store a unique ATRIP Flight Deck set of credentials. No matter how large your team is, SSO gives them seamless access to the ATRIP Flight Deck.

**3. IP WHITELIST**

IP whitelisting is a security measure that allows access to Atlas API only from specified IP addresses. By restricting access to specific, approved IP addresses, you can significantly reduce the risk of unauthorized access and potential cyber-attacks.

We upgraded this feature to make it more convenient. You can now add an unlimited number of IP addresses using netmasks to specify ranges, and include notes for easier identification.

**4. MULTI-FACTOR AUTHENTICATION (MFA)**

If enabled by your account administrator, Multi-Factor Authentication (MFA) requires users to set up two or more verification methods to gain access to the system, which significantly decreases the chance of unauthorized access.

MFA can be enabled to access the ATRIP Flight Deck account or as an extra protection method to gain access to specific features (ex., payments and top-up).

**5. FLEXIBLE PASSWORD POLICY**

If you prefer to use separate credentials to access the ATRIP Flight Deck, you can now set up custom password rules for your account.

You can adjust password requirements to your company’s standards and regulate how strong your team’s passwords should be.

**6. AUDIT LOG**

The Audit Log available on the ATRIP Flight Deck provides a comprehensive report on all system and user activities. Detailed records of user activities are made available to you to simplify reporting, compliance audits and support internal reviews.

The audit log also helps investigate incidents and verify data integrity on a regular basis.

***

These security features are designed to help you protect your data and guarantee compliance with global cybersecurity regulations.

With these features, you can easily control and manage access to your company's Atlas account both via API and the ATRIP Flight Deck.

**To enable and set up security features, visit the My Profile page on the ATRIP Flight Deck.**
