# data4governance-application
## Book Word Count Tracker
### Description
This is a personal copy of the book updater I had built myself to keep track of my reading word count. Customize this for your use by adding your goodreads ID, Drive and Sheets Authorisation for Python API.
### Tools
Written with: Python 3.6 <br />
On: Windows 7 <br />
IDE: Pycharm 2019.2.3 <br />
### Setup

#### Drive Authorisation for EZSheets
https://imgur.com/a/2Tykt6V

#### Goodreads Set Up
Account Settings > Settings > Privacy <br />
Make sure "Who can view your profile:" is set to 'anyone.' <br />
Copy your currently reading shelf's url to goodreads_id in the script <br />
If for just testing you can let this be and use my account itself. <br />

#### Lastly
Copy your credentials-sheets.json, token-drive.pickle, token-sheets.pickle to the same folder as the script  <br />
Create your sheet in your drive and copy the sheet id to sheetid in the script  <br />
Update script with your goodreads_id and sheet id.  <br />

### That's it, you are done! Run the program from command prompt!

### Known Pitfalls
Does not work if the book is not on readinglength.com <br />
readinglength.com is sometimes inaccurate about word count 
