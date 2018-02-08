# Blog_mini using docker-compose

## Forked [Blog_mini](https://github.com/xpleaf/Blog_mini) from xpleaf and updated by Vinceeee
- Modify the deploy procedure . Using docker-compose to integrate reverse_agent(nginx) , DB(MySQL) , Cache(Redis) and Application(uwsgi+app),please find the deployGuide.md for further details.

- Adding search box , which could help locate the article by content.

- Adding the function to switch background picture.

- Enhancement for user access counter , prevent the increment from refreshing by the same IP in a short while .

### Todo

- Blog import / export
- Mobile web_blog

