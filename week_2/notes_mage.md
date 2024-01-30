# Week 2: Mage Notes

Build docker image
```docker compose build```

Update mage image:
```docker pull mageai/mageai:latest```


```docker compose up```

Clean up docker objects
```docker image/volume/container prune```

## Extra stuff
Check process listening to a port
 ```sudo ss -lptn 'sport = :5432'```

Kill the process
```sudo kill <process ID>```