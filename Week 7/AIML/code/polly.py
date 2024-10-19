import boto3
import time

polly_client = boto3.Session(region_name='us-east-1').client('polly')

response = polly_client.start_speech_synthesis_task(VoiceId='Joanna',
                OutputS3BucketName='mys3bucketzzzz',
                OutputS3KeyPrefix='key',
                OutputFormat='mp3', 
                Text='This is a sample text to be synthesized.',
                Engine='neural')

taskId = response['SynthesisTask']['TaskId']

print( "Task id is {} ".format(taskId))

task_status = polly_client.get_speech_synthesis_task(TaskId = taskId)

print(task_status)