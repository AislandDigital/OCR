# OCR

This project contains source code and supporting files for a serverless 
application that you can deploy with the SAM CLI. It includes the following 
files and folders.

- ocr - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an 
API Gateway API. These resources are defined in the `template.yaml` file in this
project. You can update the template to add AWS resources through the same 
deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and 
test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI
to build and deploy serverless applications on AWS. The AWS Toolkit also adds a 
simplified step-through debugging experience for Lambda function code. See the 
following links to get started.

- [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
- [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
- [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
- [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Build OCR binaries

First you need to compile all binaries for OCR. This will build the faster 
version of OCR and a empity requirement.txt, which is required to build a layer.

```bash
cd tesseract_layer
make -f Makefile
```

or just

```bash
./build.sh  -l eng,por -m fast
```

Running into issues? Take a look at [Troubleshooting](#troubleshooting).

See this repository for any references: https://github.com/gwittchen/lambda-ocr

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an 
extension of the AWS CLI that adds functionality for building and testing Lambda
applications. It uses Docker to run your functions in an Amazon Linux 
environment that matches Lambda. It can also emulate your application's build 
environment and API.

To use the SAM CLI, you need the following tools.

- SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3 installed](https://www.python.org/downloads/)
- Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

Go to template.yaml:

- On ApiKey.value and replace the value with your api key.
- On ServerlessHttpApi.Cors.AllowOrigin remove the whitelist and change the 
correct allowed domain.(OPTIONAL)
- On ApiUsagePlan.Quota change the desired quota.(OPTIONAL)
- On ApiUsagePlan.Throttle change the desired throttle.(OPTIONAL)

To build and deploy your application for the first time, you have two options:

The guided way:

```bash
sam build --use-container
sam deploy --guided --tags YOUR_TAG_HERE
```

The config way. Here, you need first, set up the samconfig.toml:

```bash
sam build --use-container
sam deploy --tags YOUR_TAG_HERE
```

The first command will build the source of your application. The second command 
will package and deploy your application to AWS, with a series of prompts:

- **Stack Name**: The name of the stack to deploy to CloudFormation. This should 
be unique to your account and region, and a good starting point would be 
something matching your project name.
- **AWS Region**: The AWS region you want to deploy your app to.
- **Confirm changes before deploy**: If set to yes, any change sets will be 
shown to you before execution for manual review. If set to no, the AWS SAM CLI 
will automatically deploy application changes.
- **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this 
example, create AWS IAM roles required for the AWS Lambda function(s) included 
to access AWS services. By default, these are scoped down to minimum required 
permissions. To deploy an AWS CloudFormation stack which creates or modified IAM 
roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If 
permission isn't provided through this prompt, to deploy this example you must 
explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**: If set to yes, your choices will be 
saved to a configuration file inside the project, so that in the future you can 
just re-run `sam deploy` without parameters to deploy changes to your 
application.

You can find your API Gateway Endpoint URL in the output values displayed after 
deployment.

## Example of request

```bash
import requests

data = {'image64': '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', 'body': '{"image64": "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'}
headers = {'x-api-key': API_KEY}
response = requests.post(URL_ENDPOINT, json=data, headers=headers)
text = eval(response.content.decode("utf-8")

```
## Testing CORS capibility 

To test if the CORS is enable open the file index.html in your favourite browser inside the folder test_cors.

You will be faced with a blank screen and nothing else.

Open the browser tools:

Right-click > Inspect > Console.

Open the JS file in a text editor (this is it in it’s totality):

```bash
const useOCR = (args) => {
    let headers = new Headers();
    headers.append("x-api-key", "Your Key");
    headers.append('Access-Control-Allow-Origin', "*");

    return fetch("YOUR ENDPOINT/proxy", {
        method: 'POST',
        headers: headers,
        mode:"cors",
        credentials: 'same-origin',
        cache: 'no-cache',
        body: JSON.stringify(args)
      })
      .then(response => response.json())
      .then(result => result.message)
      .then(result => console.log(result))
}


```
Refresh the browser.

This is an adptation of nick script. You can check the original source [njgibbon
/
nicks-cors-test](https://github.com/njgibbon/nicks-cors-test)

## Tests

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
OCR$ sam build --use-container
```

The SAM CLI installs dependencies defined in `web_ocr/requirements.txt`, creates 
a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a 
JSON document that represents the input that the function receives from the 
event source. Test events are included in the `events` folder in this project.

**_note: Install tesseract layers dependencies running the command bellow. More on [Build OCR binaries](#build-ocr-binaries)_**

Run functions locally and invoke them with the `sam local invoke` command.

```bash
OCR$ sam local invoke OCRFunction --event events/lambda/event_image64.json
```

The SAM CLI can also emulate your application's API. Use the 
`sam local start-api` to run the API locally on port 3000.
**_note: the run in the end does not make part of the actual path on the yaml file, but is needed to keep up with {proxy+} configuration. Take a look [here](https://github.com/aws/aws-sam-cli/issues/437#issuecomment-391897052) to know more about it._**

```bash
OCR$ sam local start-api
OCR$ curl -X POST -u "x-api-key":"API_KEY" -H "Content-Type: application/json" --data @./events/api/event.json http://localhost:3000/ocr/run
```

The SAM CLI reads the application template to determine the API's routes and the 
functions that they invoke. The `Events` property on each function's definition 
includes the route and method for each path.

```yaml
Events:
  OCR:
    Type: Api
    Properties:
      Path: /ocr
      Method: post
```

### Tests for development

You can use the test's folder, to run the application in your environment or 
test the integration with AWS.
The unit tests are designed to test the behavior of the application locally, If 
you just want to deploy the stack, skip the unit tests and go to integration 
tests, they will test the integration and perform some unit test to the deployed 
endpoint.

**Limitations**: the current unit tests are used to test the application on in 
your machine.

First, create a virtual environments and install the dependencies

```bash
OCR$ pip install -r web_ocr/requirements.txt
OCR$ pip install -r web_ocr/dev-requirements.txt
OCR$ pip install -r tests/requirements.txt
```

To perform the unit tests you must install tesseracts-ocr in you local machine:

```bash
# unit test
OCR$ python -m pytest tests/unit -v
```

### Integration tests

To check if your api is running correctly on AWS type:

```bash
# integration test, requiring deploying the stack first.
# Create profile named default with your aws credentials using aws cli
# Create the env variable AWS_SAM_STACK_NAME and AWS_DEFAULT_REGION, with the name of the stack we are testing
OCR$ AWS_SAM_STACK_NAME=<stack-name> AWS_DEFAULT_REGION=<region> AWS_PROFILE=<profile> AWS_API_KEY=<api_key> python -m pytest tests/integration -v
```

## Add a resource to your application

The application template uses AWS Serverless Application Model (AWS SAM) to 
define application resources. AWS SAM is an extension of AWS CloudFormation with 
a simpler syntax for configuring common serverless application resources such as 
functions, triggers, and APIs. For resources not included in 
[the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), 
you can use standard 
[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) 
resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` 
lets you fetch logs generated by your deployed Lambda function from the command 
line. In addition to printing the logs on the terminal, this command has several 
nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you 
deploy using SAM.

```bash
OCR$ sam logs -n OCRFunction --stack-name OCR --tail
```

You can find more information and examples about filtering Lambda function logs 
in the 
[SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you 
used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name OCR --region region-name
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) 
for an introduction to SAM specification, the SAM CLI, and serverless 
application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use 
Apps that go beyond hello world samples and learn how authors developed their 
applications: 
[AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

## Troubleshooting

### Permission Denied

If run into any message related with permission on `build.sh`, when running 
_make_ on `tesseract_layer/`, just run the command bellow.

```bash
OCR/tesseract_layer$ chmod +x build.sh
```

### Environment Variables

It is a little tricky to deal with env vars with lambda locally, but aws has an
way to help with this. One can set it on the yaml file where the service is set
and overite it passing an argument to the `start-api`. Read on 
[docs](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-start-api.html)
to take doubts out.
