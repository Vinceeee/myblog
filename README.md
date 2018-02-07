# Blog_mini 
### Forked from [Blog_mini](https://github.com/xpleaf/Blog_mini)

> For issue like :
alembic.util.exc.CommandError: Can't locate revision identified by 'xxxxxxxxxxxx'    
> We need to drop the table alembic_version in the corresponding database 



## Update by Vinceeee
- Adding search box , which could help locate the article by content.

- Adding the function to switch background picture.

- Modify the deploy procedure . Using docker-compose to integrate reverse_agent(nginx) , DB(MySQL) , Cache(Redis) and Application(uwsgi+app)

- Enhancement for user access counter , prevent the increment from refreshing by the same IP in a short while .

### Todo

- Blog import / export

