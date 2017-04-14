
## Dynamic DNS using Apache Libcloud
A small, easy-to-use, Python implementation of dynamic DNS update agent.

This implementation uses [Apache Libcloud](https://github.com/apache/libcloud) and [Google Cloud DNS](https://cloud.google.com/dns/) to provide [no-ip](https://www.noip.com/)-like user experience using a robust cloud-DNS service such as Google.  


## Usage
#### Prerequisites:

- Google Cloud user account
- A GCP project with enabled billing
- An active domain name with a corresponding Zone name configured in the [Google Cloud Platform Console](https://console.cloud.google.com/networking/dns/)
- Credentials with the proper DNS permission


#### Create service account for the DNS update agent
**THIS SECTION WILL BE UPDATED SOON TO PROVIDE MORE DETAILED EXPLENATION OF HOW TO CREATE CREDENTIALS**

From [Google Cloud Platform's service accounts management](https://console.cloud.google.com/iam-admin/serviceaccounts/project), add a service account with a **DNS Administrator** role and write down the **Service Account ID**.
After the account is created, create a corresponding key in a **JSON** file format.

You'll be using the Service Accoung ID and the JSON key-file to access and update your cloud zone.

#### Clone and configure:
* Clone the repo using `git clone git@github.com:orpolaczek/libcloud-dynamic-dns.git`
* Place the JSON key-file you've downloaded from Google under the `config` folder.
* Open and edit the `config/__init__.py` file and update all it's fields to match your *Google Service Account* and *Cloud Project Name*.


**The config file**:

```python
class Config:
    DNS_USER_ID = "SERVICE_ACCOUNT_NAME@YOUR_PROJECT.iam.gserviceaccount.com" # The GCP Service Account ID
    DNS_KEY = "config/key.json" 		# The path to the JSON-key file (relative to the project's root)
    DNS_PROJECT_NAME = "YOUR_PROJECT" 	# Your Google Cloud Platform project name
    
# Example settings for creating an test.mydomain.com A record that points to your current IP
    A_RECORD_TTL_SECONDS = 3600 	# The desired TTL for your DNS record
    A_RECORD_NAME = "test" 		# The record name
    A_RECORD_ZONE_NAME = "mydomain.com." # The domain zone name (usually- the domain with an ending `.`)
    
```

## Running the update agent
* Install the dependencies using `pip install -r requirements.txt`
* Run the Python update agent using `python update_dns.py`

After running the Python file, a successfull run would look as the following:

```
➜  libcloud-dynamic-dns git:(master) ✗ python update_dns.py
Setting A record: test.mydomain.com. to point: 8.8.8.8
SUCCESS
```

In order to run the update agent periodically - use a [cronjob](https://en.wikipedia.org/wiki/Cron) :)


## Feedback
Please feel free to send feedback to <orpolaczek+libcloudddns@gmail.com> .

## Contributing
If you're willing to contribute changes/additions you've made to this code feel free to create a PR. There's always room for improvement! 

## License
This implementation of dynamic DNS using [Libcloud](https://github.com/apache/libcloud) is provided under MIT license.

Apache Libcloud is licensed under the Apache 2.0 license. For more information, please see [LICENSE](https://github.com/apache/libcloud/blob/trunk/LICENSE) and [NOTICE](https://github.com/apache/libcloud/blob/trunk/NOTICE) files on [Apache Libcloud's project](https://github.com/apache/libcloud).


