# Automod

A modular automated moderation bot for the Threadiverse that can be easily configured using a text file.

Created for [feddit.dk](https://feddit.dk) and [feddit.nu](https://feddit.nu) on Lemmy. These instances are small and no other moderation tools are necessary besides the thread scheduler at the moment, which is why it is the only module.

Modules that perform other moderation tasks can be added upon request.

## Configuration

Currently, AutoMod only supports the Lemmy API.

Set up the following environment variables by copying the provided `.env.template` file and renaming it to `.env`. Update the values in the `.env` file according to your cross-posting bot's Lemmy account and operating instance.

- `LEMMY_USERNAME`: Username for the bot's Lemmy account
- `LEMMY_PASSWORD`: Password for the bot's Lemmy account

The bot uses a `config.yaml` file to determine the actions it will carry out. Adjust the values in the `config.yaml` file according to your requirements. Make sure that the destination Lemmy communities have been created before deploying the bot.

## Examples

This configuration file tells AutoMod to create a thread named "Free Talk Friday" at 7AM CET every Friday.

```yaml
lemmy_base_uri: https://lemmy.myinstance.com # The base instance URL without anything trailing like /api/v3/
timezone: 'Europe/Berlin' # Timezone as defined in the tz database: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

scheduled_posts:
  - community: 'my_lemmy_community'
    title: 'Free Talk Friday'
    content: |
      ## Happy Friday!

      **This is the weekly free talk thread at My Lemmy Community.**

      Please feel free to discuss anything and everything happening in your life! Remember to respect the forum rules:
      - Don't post things that are related to the Drama Controversy of $CURRENTYEAR.
      - Everything you post on the Internet will be here forever. Don't reveal any personally identifiable information.
    external_link: # Leave empty to not add a link
    frequency_unit: 'weeks' # minutes, hours, days, weeks
    frequency: 1 # Schedule the post every X minutes/hours/days/weeks
    day: 'friday' # Day of the week if frequency_unit is week
    time: '07:00' # 24-hour time if frequency is 'day' or 'week'. Minutes or seconds otherwise. See https://schedule.readthedocs.io/en/stable/examples.html for more info
```