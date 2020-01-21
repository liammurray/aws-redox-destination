# -*- mode: Makefile -*-
#

PACKAGE_OUTPUT_BUCKET = nod15c.lambda
STACK_NAME = $(shell basename $(CURDIR))
OUTPUT_TEMPLATE = .packaged.yaml

# TODO Should exclude test
source_files := $(wildcard redox/*.py)
source_manifests := redox/requirements.txt

# List of targets that are not files
.PHONY: \
	validate \
	test \
	build \
	clean \
	package \
	deploy \
	errors \
	output

SHELL=/usr/bin/env bash -o pipefail

test:
	@set -e; for dir in $(subdirs); do \
		cd $$dir; \
		pytest; \
	 done

clean:
	@rm -rf .aws-sam
	@rm -f $$OUTPUT_TEMPLATE

build:
	sam build

api:
	sam local start-api

validate:
	sam validate

# Build if sam template or any source file is updated
.aws-sam/build: template.yaml $(source_files) $(source_manifests)
	sam build

$(OUTPUT_TEMPLATE): .aws-sam/build
	sam package \
		--output-template-file $(OUTPUT_TEMPLATE) \
	  --s3-bucket $(PACKAGE_OUTPUT_BUCKET)

package: $(OUTPUT_TEMPLATE)

deploy: $(OUTPUT_TEMPLATE)
	sam deploy \
		--template-file $(OUTPUT_TEMPLATE) \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_NAMED_IAM

# changeset: $(OUTPUT_TEMPLATE)
# 	@aws cloudformation deploy \
# 		--no-execute-changeset \
# 		--template-file $(OUTPUT_TEMPLATE) \
# 		--stack-name $(STACK_NAME) \
# 		--capabilities CAPABILITY_NAMED_IAM

output:
	@aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[].Outputs' \
		--output table

destroy:
	@aws cloudformation delete-stack \
			--stack-name $(STACK_NAME)

errors:
	@aws cloudformation describe-stack-events \
			--stack-name $(STACK_NAME) \
			| jq '.StackEvents[]|select(.ResourceStatus|index("FAILED"))'

outputs:
	@aws cloudformation describe-stacks \
			--stack-name $(STACK_NAME) \
			| jq '.Stacks[].Outputs'
