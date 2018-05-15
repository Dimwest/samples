#!/bin/bash
if [ $TRAVIS_BRANCH = "test" ]; then 
  echo 'On branch test'
  cd flyway-5.0.7 && ./flyway -url=$STAGING_URL -user=$STAGING_USER -password=$STAGING_PW -locations=filesystem:../analyst/dwh/incremental_migrations -schemas=$SCHEMAS migrate
elif [ $TRAVIS_BRANCH = "master" ]; then
  echo 'On branch master' 
  cd flyway-5.0.7 && ./flyway -url=$PROD_URL -user=$PROD_USER -password=$PROD_PW -locations=filesystem:../analyst/dwh/incremental_migrations -schemas=$SCHEMAS migrate
fi
