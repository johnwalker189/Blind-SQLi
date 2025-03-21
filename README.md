# My (Uncompleted) Tool For Testing Error-Based SQLi Vulnerabilities Combining With SSRF
Yes, I tried to reinvent the wheel that is Error-based SQL injection for a lab I'm trying to solve. Consider it a hobby project from a novice that strives to become a decent Pentester. I have also left a port scanning script that takes advantage of SSRF in there.

![image](https://github.com/user-attachments/assets/9eaa578d-a535-4b2b-8507-ce580c58506a)

## Requirements

In the process of developing this tools, I made use of Python and many of its library. I've already put them inside the `.venv` folders, but if you can't use them for some reasons I've also provided a `requirements.txt` file. 

## Getting started

To get started with this project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/johnwalker189/Blind-SQLi.git
   ```
2. Set up the variables:
   There isn't much to set up, but there are three main variables that you have to look out for:
   - PREFIX_URL: This is set at every stages of SQLi, so you will have to change the payload manually. It is used to forge the link that will exploit BOTH the SSRF and SQLi vulnerability.
   - BASE_URL: The link of the web that's having the vuln.
   - wrong_indicator: The string of words that indicates the *false* state, which will be used to brute-force the way through the database's table names and such.

## So, how does this thing actually good.

Well, I wish I knew.

Anyways, this "tool" will only work if you've already found an endpoint that has the SSRF vulnerability. After generating the `PREFIX_URL` varible (you actually only have to change the `http://localhost:8888/post.php?id=1` part, the text afterwards can be left the way it is), this tool will take advantage of the SQLi vulnerability to check for table names or column names and such. I initially brute-forced my way through 96 characters in the ASCII table to check for the names, but then realized that using Bit Shifting would greatly accelerate the process.

Yeah, that's probably all of it. 

If you somehow stumbled upon this and wish to improve this thing, here's what you can do:

- Fork the repo.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Push your changes to your forked repository.
- Submit a pull request to the main repository.

## Last words

Thanks for visiting this repository, people! Honestly, I think I still have a **very** long way to go. If you wish to contact me for a deeper chat, my discord ID is @johnwalker189. 

I hope I can come back with a new project soon enough, ehe.

Happy hacking!
   
