Robobrain Onboarding Docs
===================

#### Table of Contents
  - [For the New Developer](#for-the-new-developer)
      - [Introduction](#introduction)
      - [Technology Stack](#technology-stack)
      - [How to get the code running locally](#how-to-get-the-code-running-locally)
      - [How to use AWS to deploy](#how-to-use-aws-to-deploy)
      - [Who you can get in touch with](#who-you-can-get-in-touch-with)
  - [For the Old Developer](#for-the-old-developer)
      - [Things to give New Users](#things-to-give-new-users)
      - [Adding New Users](#adding-new-users)
      - [Future Administrative Work](#future-administrative-work)

-------------

For the New Developer
-------------
#### Introduction
[**Robobrain**](robobrain.me) is a project that serves Twitter-like feeds of various things learned by the research project that contribute to it. It tags special concepts that the robot learns like *book* or *grasp* and creates a graphical association for them. Our web interface allows us to view the infinite feed, upvote and downvote elements, comment using [Disqus](https://disqus.com/) and view the underlying graph structure <sup>Coming Soon</sup>



#### Technology Stack

Technologically, Robobrain is hosted on private Github repositories under the organization **RoboBrainCode**. We have separate repositories for the Backend, Frontend and a client-side interface through which new feeds can be added.

<img src="https://github.com/RoboBrainCode/Docs/blob/master/diagram.jpg?raw=true" width="700px"/>

Our Backend stack is in **Django**, a **Python** based web framework, which connects to our feed database, in **MongoDB** and further, our graph database, in **Neo4j** <sup>Coming Soon</sup>.

Our Frontend stack is in **Angularjs**, a **Javascript** based front-end framework by Google, generated and scaffolded by **Yeoman**. We use **Grunt** as our build system, and **node** and **bower** as our package managers. For our graph visualization, we use **D3js** <sup>Coming Soon</sup>.

To deploy, we use **nginx** as our webserver, which serves the static files built by Grunt, and uses **uwsgi** to interface with Django.

> **Note:** If any portion of the tutorial below is incorrect or not functional, contact Deedy (dd367@cornell.edu) immediately.



####  How to get the code running locally
 1. Add new user's Github account to the organization **RoboBrainCode**.

 2. Clone the SSH URL of the repositories [**Backend**](https://github.com/RoboBrainCode/Backend) and [**Frontend**](https://github.com/RoboBrainCode/Frontend).
 >  SSH URL eg. `git@github.com:RoboBrainCode/Backend.git`

 3. For Frontend, navigate to the root directory of the repository, and run `npm install` and `bower install`. If everything runs smoothly, run `grunt serve` and you should be able to see a local version running on http://localhost:9000.

 4. After you made your changes, and they look functional on local, merge your changes with the `test` branch.

 5. After following the instructions in the second part of this guide, you should have made sure your changes are working at http://test.robobrain.me.

 5. If they work correctly on `test`, merge to the `production` branch. Then follow more instructions in the second part of the guide to finish your deploy.
 > **Important:** Currently, be careful to not overwrite the `Gruntfile.js` on the `production` branch or it will use the test database instead of the production one.


 6.  For Backend, run `sudo pip install -r requirements.txt` to install all your Python dependencies.

 7.  If all goes well, run `python manage.py runserver` and you should be able to see your Django backend running on http://localhost:8000.
 > **Note:** We are currently fixing an issue with the `uwsgi` dependency, so this might not work.

 8.  If they work correctly on `test`, merge to the `production` branch. Then follow more instructions in the second part of the guide to finish your deploy.
 > **Important:** Currently, be careful to not overwrite the `manage.py` on the `production` branch or it will use the test database instead of the production one.



####  How to use AWS to deploy

 1. Get your username and password set up for accessing the Amazon AWS dashboard and console. From here, you can look at all our running instances, see information about them, and more.

 2. After your user accounts are set up on the instances, note your username, typically your firstname. For the purpose of this guide, we'll assume the username is `deedy`. Your default password will be `robobrain`.

 3. Obtain `.pem`  files to access the Amazon AWS EC2 instances.
>  Robobrain runs on Amazon Web Services (AWS)'s Elastic Cloud 2 (EC2) instances, or virtual machines. These are typically accessed by `ssh`ing into the instance with special `.pem` files as authorization.
 4. Keep you all your `.pem` files in a safe directory, say `~/robobrain/` and rename them `www.pem`, `mongo-test.pem`, and `mong-prod.pem` as appropriate.

 5.  Add the following aliases to your shell rc file, usually `~/.bashrc` or `~/.zshrc`:
 ```bash
alias ssh-robobrain-www-prod='ssh -i ~/robobrain/www.pem ec2-54-218-14-187.us-west-2.compute.amazonaws.com -l deedy'
alias ssh-robobrain-www-test='ssh -i ~/robobrain/www.pem ec2-54-218-20-10.us-west-2.compute.amazonaws.com -l deedy'
alias ssh-robobrain-mongo-prod='ssh -i ~/robobrain/mongo-prod.pem ec2-54-186-129-44.us-west-2.compute.amazonaws.com -l ec2-user'
alias ssh-robobrain-mongo-test='ssh -i ~/robobrain/mongo-test.pem ec2-54-186-47-107.us-west-2.compute.amazonaws.com -l ec2-user'
 ```
 Now, restart your shell. After this, you'll be able to use the commands `ssh-robobrain-www-prod` (The [production](robobrain.me) website instance), `ssh-robobrain-www-test` (The [test](test.robobrain.me) website instance), `ssh-robobrain-mongo-prod` (The production mongoDB instance) and `ssh-robobrain-mongo-test` (The test mongoDB instance) to access the appropriate instances.
 6.  Now, run `ssh-robobrain-www-test` to login to the test.robobrain instance. You should see a beautiful [solarized](http://ethanschoonover.com/solarized) terminal with a prompt, and you should be automatically in the directory `/var/www` which contains 2 folders - `Frontend` and `Backend`, our two repositories.

 7.  Firstly, you'll want to associate your Github account with the one on the instance. To do this, follow the tutorial here - [Generating SSH Keys - Github](https://help.github.com/articles/generating-ssh-keys).

 8. For Frontend, guide yourself to `/var/www/Frontend/` and pull the changes you made to the `test` branch. Run a `grunt build`. This may take up to 8 minutes, because compressing images takes a long time. To speed this up, comment out the line that contains `'imagemin',` under concurrent > dist, in `Gruntfile.js`. This compiles the optimized static content to the  `/var/www/Frontend/dist` folder, and serves it live on `http://test.robobrain.me`.

 9.  For Backend, guide yourself to `/var/www/Frontend/` and pull the changes you made to the `test` branch. Run `uwsgi --reload /tmp/robobrain-master.pid` to see your backend changes reflected at `http://test.robobrain.me:3000`

 10.  For deploying on production, the instructions remain pretty much identical, except all the commands should be run in the `production` branch.

 11.  If anything goes wrong in the final deploy process, check one of the following logs:
         - nginx access log - `/var/log/nginx/access.log`
         - nginx error log - `/var/log/nginx/error.log`
         - uwsgi - `/var/log/uwsgi/robobrain.log`



####  Who you can get in touch with

 - **Deedy Das (dd367@cornell.edu)** - Full stack developer, worked on all the system administration and deployment stuff, did initial site design and frontend
 - **Ashesh Jain (ashesh@cs.cornell.edu)** - Backend developer, started the Django backend after previously having written the Rails backend
 - **Kevin Lee (kkl53@cornell.edu)** - Frontend developer, started the Angular/Yeoman frontend
 - **Ozan Sener (os79@cornell.edu)** - Database administrator, in charge of the mongoDB instances and wrote the Client repo to add feeds to the DB
 - **Aditya Jami (adityajami@gmail.com)** - Amazon AWS guy, set up AWS and got everybody initial access to deployment

----------



For the Old Developer
-------------
####  Things to give New Users

 1. An account with Amazon AWS.

 2. The 3 `.pem` files needed to access the 4 EC2 instances - `www-test`, `www-large`, `mongo-test` and `mongo-prod`.

 3. Add them to Github organization, giving them access to the repositories.



####  Adding New Users

 1. The following instructions should be executed both for `www-test` and `www-large` for adding a new user, say `deedy`.

 2. In the EC2 instance, run `sudo adduser deedy` to add the user, putting in his full name, his school for the field `Room number` and his actual phone number. Set his default password to be `robobrain`.

 3.  Run `sudo usermod -g developers deedy` to add him to the  group `developers`. Ensure he is in the group by running `members developers`.

 4. Run `/usr/sbin/visudo` and give the user root privileges by adding the line `deedy   ALL=(ALL:ALL) ALL` below all the other usernames in the file.

 5. Change yourself to be the new user by running `sudo su - deedy` and navigate to the home directory with `cd ~`

 6. Run the following commands to allow him to login to the instance as himself:
    ```bash
    mkdir .ssh
    chmod 700 .ssh
    touch .ssh/authorized_keys
    chmod 600 .ssh/authorized_keys
    echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsslXUjdR/aNh+Ygdf6HjSA6mmyvjpkKzht+lJnTx0b2ZS0cBnzLsL/fQ+qlY+HANB7pcgYbk6p/z9oeZ0BC75a/UZHDQfBWCoAyQg2w+AVpSKn0BwfgnN741NgYGGRft8nturpjB4RZl2xHiLrdBhOFpD27r7ZHMvreE8jHgDDySZztBYzB1waLerM63Wk07RQU6V/J7AUEWyhCKPRzfD7tltUwvdGtzBSpU0xvmIgJz+b/7QlNfVRYouf5P4vt5leO176WlNOgOfKtJvalLBTJ9vgh7/9GAKQH6esuJzg+qaPXnnBVAdXP+994CmjyTpMpxR+x/H+ssNbLs4dndp www' > .ssh/authorized_keys
    ```


 7. Now, copy your dot files to enable oh-my-zsh and solarized vim for the new user by executing the following:
    ```bash
    sudo cp -R ~/.vimrc /home/deedy/
    sudo cp -R ~/.zshrc /home/deedy/
    sudo cp -R ~/.oh-my-zsh /home/deedy/
    ```
Proceed to set the new user's default shell to `zsh` by running `chsh -s /bin/zsh`.



####  Future Administrative Work

 1. Iron out specifications as to what branches will contain what such that overwrites on a certain file are not an issue, and do not change the backend database.

 2. Figure out auto reloading of Django with uwsgi again.

 3. Add Github hooks to auto-pull and update the live site every time a merge is made to the`test` or `production` branches.

 4. Alpha-test the on-boarding procedure on current members to make sure everything works and keep this doc updated.

 5. Figure out the correct `nginx`, `uwsgi` and permission settings on the instances.

 6. Not so distant future - figure out how we are going to do testing. As our code get's bigger, we cannot blindly launch.

 7. Distant future - possibly add Phabricator as a code review tool.



----------
