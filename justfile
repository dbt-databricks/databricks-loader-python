# Local Variables:
# mode: justfile
# End:

set dotenv-load
set export

arch := `uname -m`

test-mac:
	docker build -t dataloader .
	docker run -d -v /Users/fuzezhong/Documents/GitHub/dbt-databricks/databricks-loader-python/data:/var/task/dataloader/data -v /Users/fuzezhong/Documents/GitHub/dbt-databricks/databricks-loader-python/log:/var/task/dataloader/log dataloader:latest

build-whole:
	docker build -f Dockerfile.sample -t dataloader .
	docker tag dataloader:latest 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest
	docker push 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest

build:
	docker build -f Dockerfile -t dataloader .
	docker tag dataloader:latest 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest
	docker push 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest

volums:
	docker volume create datawaves-data

run:
	docker pull 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest
	docker run -d -v /home/ec2-user/data:/var/task/dataloader/data -v /home/ec2-user/log:/var/task/dataloader/log 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest

buildenv:
	docker build -f Dockerfile.pyenv -t pyenv .
	docker tag pyenv:latest 164267459440.dkr.ecr.us-west-2.amazonaws.com/pyenv:latest
	docker push 164267459440.dkr.ecr.us-west-2.amazonaws.com/pyenv:latest