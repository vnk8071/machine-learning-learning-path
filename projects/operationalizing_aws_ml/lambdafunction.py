import json
import boto3

print('Loading Lambda function')

runtime = boto3.Session().client('sagemaker-runtime')
endpoint_Name = 'pytorch-inference-2023-09-14-02-38-59-976'


def lambda_handler(event, context):
    print('Context: ', context)
    print('EventType: ', type(event))
    bs = event
    runtime = boto3.Session().client('sagemaker-runtime')

    response = runtime.invoke_endpoint(
        EndpointName=endpoint_Name,
        ContentType="application/json",
        Accept='application/json',
        Body=json.dumps(bs)
    )

    result = response['Body'].read().decode('utf-8')
    sss = json.loads(result)

    return {
        'statusCode': 200,
        'headers' : {'Content-Type' : 'text/plain', 'Access-Control-Allow-Origin' : '*'},
        'type-result' : str(type(result)),
        'COntent-Type-In' : str(context),
        'body' : json.dumps(sss)
    }
