# Balloon Shooter Game

A simple balloon shooting game that can be hosted on AWS S3.

## Game Features

- Shoot balloons with a cannon
- Random colored balloons
- Special gold balloons worth extra points
- Progressive difficulty levels
- High score tracking

## How to Play

- Use left and right arrow keys to move the cannon
- Press spacebar to shoot
- Hit regular balloons for 10 points
- Hit special gold balloons for 30 points
- Advance through levels by earning points

## Hosting on AWS S3

### Prerequisites

1. AWS account
2. AWS CLI installed and configured
3. S3 bucket created

### Deployment Steps

1. Edit the `deploy-to-s3.sh` script and replace `your-bucket-name` with your actual S3 bucket name.

2. Make the script executable:
   ```
   chmod +x deploy-to-s3.sh
   ```

3. Run the deployment script:
   ```
   ./deploy-to-s3.sh
   ```

4. Configure your S3 bucket for static website hosting:
   - Go to the AWS Management Console
   - Navigate to S3 and select your bucket
   - Go to the "Properties" tab
   - Scroll down to "Static website hosting" and click "Edit"
   - Select "Enable" and set "Index document" to "index.html"
   - Save changes

5. Your game will be available at:
   ```
   http://your-bucket-name.s3-website-your-region.amazonaws.com/
   ```

## Local Development

To test the game locally, simply open the `index.html` file in a web browser.