# Local Variables:
# mode: justfile
# End:

set dotenv-load
set export

arch := `uname -m`

test:
	docker build -t dataloader .
	docker run -d dataloader:latest

build:
	docker build -t dataloader .
	docker tag dataloader:latest 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest
	docker push 164267459440.dkr.ecr.us-west-2.amazonaws.com/dataloader:latest

buildenv:
	docker build -t pyenv .
	docker tag pyenv:latest 164267459440.dkr.ecr.us-west-2.amazonaws.com/pyenv:latest
	docker push 164267459440.dkr.ecr.us-west-2.amazonaws.com/pyenv:latest