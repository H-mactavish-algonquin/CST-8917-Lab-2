from datetime import timedelta
import azure.functions as func
import azure.durable_functions as df
import asyncio


async def orchestrator_function(context: df.DurableOrchestrationContext):
    retry_options = df.RetryOptions(
        first_retry_interval=timedelta(minutes=1),
        max_number_of_attempts=3
    )

    image_blob = context.get_input()

    # Process images in parallel using asyncio.gather
    resized_image_task = context.call_activity_with_retry(
        'ResizeImage', retry_options, image_blob)
    grayscale_image_task = context.call_activity_with_retry(
        'GrayscaleImage', retry_options, image_blob)
    watermarked_image_task = context.call_activity_with_retry(
        'WatermarkImage', retry_options, image_blob)

    # Wait for all tasks to complete
    await asyncio.gather(resized_image_task, grayscale_image_task, watermarked_image_task)

    resized_image = resized_image_task.result()
    grayscale_image = grayscale_image_task.result()
    watermarked_image = watermarked_image_task.result()

    return watermarked_image

main = df.Orchestrator.create(orchestrator_function)
