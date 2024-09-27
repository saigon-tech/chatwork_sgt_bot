# SGT Chatwork Bot

A modular, extensible chatbot for SGT Team that responds to mentions in Chatwork rooms and performs predefined actions.

## Key Features

- Mention-based interaction
- Modular architecture for easy extension
- GPT-3.5 powered command interpretation
- Asynchronous processing with Celery

## Quick Start with Makefile

This project includes a Makefile to simplify common development tasks. Here are some useful commands:

1. Build the Docker image:
   ```
   make build
   ```

2. Start the application:
   ```
   make up
   ```

3. Stop the application:
   ```
   make down
   ```

4. Run tests:
   ```
   make test
   ```

5. Access the container shell:
   ```
   make connect
   ```

6. View application logs:
   ```
   make logs
   ```

Remember to set up your `.env` file with the necessary environment variables before running these commands. Refer to the
`.env.example` file for the required variables.

## How to Add a New Action

1. Create `src/actions/action_<your_action_name>.py`
2. Define a new class inheriting from `Action`:

```python
from src.actions.action_decorator import Action, ActionRegistry
from src.utils.web_utils import WebHelper


@ActionRegistry.register('your_action_name', 'Description of your action')
class YourActionClass(Action):
    def execute(self, room_id: str, account_id: str, message: str, web_helper: WebHelper) -> str:
        # Implement your action logic here
        return "Your action response"
```

3. The `@ActionRegistry.register` decorator automatically registers your action.
4. Implement your logic in the `execute` method.
5. Return a string as the response.
6. Your new action is now available in Chatwork using the registered command name.

### Parameter Explanations:

- `your_action_name`: The command name users will use to trigger your action in Chatwork.
  Example: 'weather_forecast'
- `Description of your action`: A brief explanation of what your action does.
  Example: 'Get the weather forecast for a specified city'
- `room_id`: The ID of the Chatwork room where the action was triggered.
- `account_id`: The ID of the Chatwork user who triggered the action.
- `message`: The full message content that triggered the action.
- `web_helper`: An instance of the WebHelper class for making web requests.

For more details on using the WebHelper class, refer to the [WebHelper.md](./WebHelper.md) file.

## Contributing

Contributions are welcome! Please submit a Pull Request.

### Ideas for New Actions

Here are some ideas for actions you can build to enhance the SGT Chatwork Bot:

| **Category**                           | **Action**                     | **Description**                                                                             | **Command**                     |
|----------------------------------------|--------------------------------|---------------------------------------------------------------------------------------------|---------------------------------|
| **Team Building & Engagement**         | Daily Icebreakers or Fun Facts | Sends fun questions or facts to engage the team.                                            | `/daily_icebreaker`             |
|                                        | Gamification of Tasks          | Tracks task completion and assigns points to team members.                                  | `/task_leaderboard`             |
|                                        | Recognition and Shoutouts      | Allows team members to give kudos to colleagues for good work.                              | `/give_kudos @username reason`  |
| **Wellness & Productivity**            | Regular Break Reminders        | Reminds team members to take regular breaks to avoid burnout.                               | `/schedule_breaks interval`     |
|                                        | Mood Check-ins                 | Periodically asks team members about their mood and gauges team morale.                     | `/mood_checkin`                 |
|                                        | Focus Sessions                 | Helps team members set focus periods to work without distractions.                          | `/start_focus_session duration` |
| **Learning & Development**             | Knowledge Sharing              | Encourages sharing useful tips, tutorials, or best practices.                               | `/share_tip`                    |
|                                        | Random Code Review             | Randomly selects code snippets for team review to encourage continuous improvement.         | `/random_review`                |
|                                        | Pair Programming Sessions      | Schedules pair programming sessions to promote collaboration.                               | `/schedule_pair_programming`    |
| **Communication & Feedback Loops**     | Anonymous Feedback             | Allows submission of anonymous feedback on various team topics.                             | `/submit_feedback topic`        |
|                                        | Pulse Surveys                  | Periodically sends out short surveys to gauge team sentiment on specific topics.            | `/send_survey question`         |
|                                        | Daily Stand-up Automation      | Automates daily standups, collecting updates from team members and summarizing them.        | `/daily_standup`                |
| **Productivity & Project Improvement** | Retrospective Sessions         | Schedules retrospectives and gathers feedback on what went well and what could be improved. | `/schedule_retro topic`         |
|                                        | Sprint Planning Assistance     | Assists with organizing sprint tasks, reviewing backlogs, and prioritizing them.            | `/start_sprint_planning`        |
| **Knowledge Base & Documentation**     | Documentation Requests         | Retrieves documentation or internal knowledge base articles.                                | `/request_doc`                  |
|                                        | FAQs and Onboarding            | Provides answers to frequently asked questions, especially useful for new members.          | `/faq topic`                    |
| **Team Communication and Alignment**   | Quick Polls                    | Creates quick polls to gather team consensus on decisions.                                  | `/create_poll question`         |
|                                        | Meeting Summary Generator      | Fetches a summary of previous meetings or tasks discussed.                                  | `/meeting_summary meeting_id`   |
|                                        | Q&A Sessions                   | Starts live Q&A sessions for team members to ask and answer questions on specific topics.   | `/qna_session topic`            |
| **Miscellaneous Team Improvement**     | Random Team Lunch Pairings     | Randomly pairs team members for lunch meetings to encourage bonding.                        | `/random_lunch_pairing`         |
|                                        | Inspirational Quotes           | Sends daily motivational or inspirational quotes to the team.                               | `/daily_quote`                  |

Feel free to implement any of these ideas or come up with your own to improve team productivity and collaboration!
