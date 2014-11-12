Robobrain Onboarding Docs
===================

#### Table of Contents
  - [For the New Developer](#for-the-new-developer)
      - [Introduction](#introduction)
      - [Technology Stack](#technology-stack)
      - [How to get the code running locally](#how-to-get-the-code-running-locally)
      - [Iterating and Deploying](#iterating-and-deploying)
      - [How to set up AWS access](#how-to-set-up-aws-access)
      - [Who you can get in touch with](#who-you-can-get-in-touch-with)
  - [For the Old Developer](#for-the-old-developer)
      - [Things to give New Users](#things-to-give-new-users)
      - [Adding New Users](#adding-new-users)
      - [Future Administrative Work](#future-administrative-work)
      - [Bugs and Fixes](#bugs-and-fixes)

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

To deploy, we use **nginx** as our webserver, which serves the static files built by Grunt, and uses **uwsgi** to interface with Django and we use **fabric** as a deployment tool.

> **Note:** If any portion of the tutorial below is incorrect or not functional, contact Deedy (dd367@cornell.edu) immediately.



####  How to get the code running locally
 1. Add new user's Github account to the organization **RoboBrainCode**.

 2. Clone the SSH URL of the repositories [**Backend**](https://github.com/RoboBrainCode/Backend) and [**Frontend**](https://github.com/RoboBrainCode/Frontend).
 >  SSH URL eg. `git@github.com:RoboBrainCode/Backend.git`

 3. For Frontend, navigate to the root directory of the repository, and run `npm install` and `bower install`. If everything runs smoothly, run `grunt serve` and you should be able to see a local version running on http://localhost:9000. 
	 	> **Note:** By default, this frontend would connect to the `test.robobrain.me` backend. To develop full stack locally, simply run `grunt serve:uselocal` after running your Django server locally, presumably on the default port 8000, to develop backend and frontend simultaneously. 
 
 7.  For Backend, run `sudo pip install -r requirements.txt` to install all your Python dependencies.

 8.  If all goes well, run `python manage.py runserver` and you should be able to see your Django backend running on http://localhost:8000.

 9.  You should do your development on a separate feature branch `myfeature`. After testing locally, you should merge the branch to `master` by checking out `master` and executing `git merge --no-ff myfeature`. More details can be found here: [A Successful Branching Model](http://nvie.com/posts/a-successful-git-branching-model/).
 
####  Iterating and Deploying 

 10. At this point, you should probably proceed with the steps in this section - [How to use AWS to deploy](#how-to-use-aws-to-deploy) to ensure access to the AWS instances. Ensure you're on the `master` branch. 
 
 11. Run `fab test_deploy:deedy` if your username is `deedy` to deploy your changes to http://test.robobrain.me. 
 
 
	> **Note:** The fab scripts are currently in their beginning stages and may run into issues with unexpected behavior such as addition of new libraries.

	> **Note:** The Frontend deployment has an additional speed option. By default, it uses `fast` which deploys the Frontend to the server and builds it without optimizing new images. To disable this, just run `fab test_deploy:deedy,slow`. <sup>Untested</sup>

 
 11. If everything works there, run `fab prod_deploy:deedy` (if `deedy` is your username) to deploy to http://robobrain.me.

 
	> **Note:** By default, without a specified username, fab uses `ubuntu`. On `test_deploy`, this automagically works without requiring any other forms of authentication. On `prod_deploy` however, this doesn't work because it cannot authenticate our git account through fab for some reason. 




####  How to set up AWS access

 1. Get your username and password set up for accessing the Amazon AWS dashboard and console. From here, you can look at all our running instances, see information about them, and more.

 2. After your user accounts are set up on the instances, note your username, typically your firstname. For the purpose of this guide, we'll assume the username is `deedy`. Your default password will be `robobrain`.

 3. Obtain `.pem`  files to access the Amazon AWS EC2 instances.
>  Robobrain runs on Amazon Web Services (AWS)'s Elastic Cloud 2 (EC2) instances, or virtual machines. These are typically accessed by `ssh`ing into the instance with special `.pem` files as authorization.
 4. Keep you all your `.pem` files in a safe directory, say `~/robobrain/` and rename them `www.pem`, `mongo-test.pem`, and `mong-prod.pem` as appropriate.

 5.  Add the following aliases to your shell rc file, usually `~/.bashrc` or `~/.zshrc`:
 ```bash
alias ssh-robobrain-www-prod='ssh -i ~/Dev/PR-Research/robobrain/www.pem ec2-54-68-27-137.us-west-2.compute.amazonaws.com -l deedy'
alias ssh-robobrain-www-test='ssh -i ~/Dev/PR-Research/robobrain/www.pem ec2-54-218-20-10.us-west-2.compute.amazonaws.com -l deedy'
alias ssh-robobrain-mongo-prod='ssh -i ~/Dev/PR-Research/robobrain/mongo-prod.pem ec2-54-186-129-44.us-west-2.compute.amazonaws.com -l ec2-user'
alias ssh-robobrain-mongo-test='ssh -i ~/Dev/PR-Research/robobrain/mongo-test.pem ec2-54-186-47-107.us-west-2.compute.amazonaws.com -l ec2-user'
 ```
 Now, restart your shell. After this, you'll be able to use the commands `ssh-robobrain-www-prod` (The [production](robobrain.me) website instance), `ssh-robobrain-www-test` (The [test](test.robobrain.me) website instance), `ssh-robobrain-mongo-prod` (The production mongoDB instance) and `ssh-robobrain-mongo-test` (The test mongoDB instance) to access the appropriate instances.
 6.  Now, run `ssh-robobrain-www-test` to login to the test.robobrain instance. You should see a beautiful [solarized](http://ethanschoonover.com/solarized) terminal with a prompt, and you should be automatically in the directory `/var/www` which contains 2 folders - `Frontend` and `Backend`, our two repositories.

 7.  Firstly, you'll want to associate your Github account with the one on the instance. To do this, follow the tutorial here - [Generating SSH Keys - Github](https://help.github.com/articles/generating-ssh-keys).
	 	> **Note:** This tutorial asks you to set a secure password, but now, during the `fab` deploy process, this would require you to enter a password 3-4 times during every deploy. To avoid this annoyance, simply set no text as your `ssh` password for your key.

 8. For both Backend and Frontend, we deploy with `fab`. To view the details of this process, simply open up the `fabfile.py` in the root directory of every repository. It is a very simple Python script wrapper for SSHing and running shell commands.

 11.  If anything goes wrong in the final deploy process, check one of the following logs or contact one of the people below:
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

 2. The 2 `.pem` files needed to access the 2 EC2 instances - `mongo-test` and `mongo-prod`.
	 > **Note:** Now,  `www.pem`, for `www-test`, `www-large` is a part of the Backend repository.

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


 7. Now, copy the dot files from an existing user to enable oh-my-zsh and solarized vim for the new user by executing the following:
    ```bash
    sudo cp -R /home/<existinguser>/.vimrc ~/
sudo cp -R /home/<existinguser>/.zshrc ~/
sudo cp -R /home/<existinguser>/.oh-my-zsh ~/
    ```
Proceed to set the new user's default shell to `zsh` by running `chsh -s /bin/zsh`.



####  Future Administrative Work 

 1. Figure out an effective way to update other team members on Django dependencies, as well as auto deploy new dependencies to the servers.
 
 2. Serve the backend through a subdomain like `api.robobrain.me` or a URL such as `robobrain.me/api/` instead of the hacky separate `3000` port.

 3. Get the entire team on [Slack](https://slack.com/).

 4. Alpha-test the on-boarding procedure on current members to make sure everything works and keep this doc updated.

 5. Figure out the correct `nginx`, `uwsgi` and permission settings on the instances.

 6. Not so distant future - figure out how we are going to do testing. As our code get's bigger, we cannot blindly launch.

 7. Distant future - possibly add Phabricator as a code review tool.



----------

####  Bugs and Fixes

 1. Add a video player library - either video.js or flowplayer - to wrap the videos and make them cross-browser compatible, and dynamically loaded.

 2. Some of the API content returns  `#$` in the text. These hashtags should not be stripped and bolded and queryable.

 3. Batching the database calls loses the order that we need. Re-establish that order.

 4. Currently, CORS access is given to all URLs on production. This is a changeable setting in Django.

 5. SVGs on the Frontend don't build correctly to the right location.

 6. Some of the `sourceText` labels overflow on mobile. 

----------
