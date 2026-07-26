"""
Discord Bot for PlacementPro Free ATS Tool.
Deploy to university CS club servers for organic growth.

Usage:
1. /checkresume - Analyze a resume attachment
2. /score - Quick score for pasted text
3. /link - Get link to full web app

Setup:
1. Create Discord bot at discord.com/developers
2. Add to university CS club servers
3. Run: python discord_bot.py
"""

import discord
from discord import app_commands
from discord.ext import commands
import re
from typing import Dict, Any


class FreeATSChecker:
    """Same algorithmic checker as free_ats_tool.py but for Discord."""

    def check(self, text: str) -> Dict[str, Any]:
        score = 100
        issues = []

        # Tables
        if re.search(r'[\|\t]{2,}', text):
            issues.append("🔴 Tables detected - ATS can't parse them")
            score -= 20

        # Columns
        if re.search(r'\S{20,}\s{4,}\S{20,}', text):
            issues.append("🔴 Multi-column layout - causes parsing errors")
            score -= 15

        # Special chars
        if re.search(r'[\u25A0-\u25FF\u2B50\u2705\u2714\u2716\u26A0]', text):
            issues.append("🟠 Special characters/emojis found")
            score -= 10

        # Weak bullets
        weak_patterns = [
            r'(?i)^responsible for\b',
            r'(?i)^helped with\b',
            r'(?i)^assisted in\b',
            r'(?i)^worked on\b',
        ]
        weak_count = sum(1 for p in weak_patterns if re.search(p, text))
        if weak_count > 2:
            issues.append(f"🟡 {weak_count} weak bullet points")
            score -= 10

        # No metrics
        metric_patterns = [r'\d+%', r'\$\d+', r'\d+x\b']
        metric_count = sum(1 for p in metric_patterns if re.search(p, text))
        if metric_count < 2:
            issues.append("🟡 Few quantified achievements")
            score -= 10

        # Email check
        if not re.search(r'[\w.-]+@[\w.-]+\.\w+', text):
            issues.append("🟠 No email address found")
            score -= 10

        return {
            "score": max(0, score),
            "issues": issues,
            "passed": len([i for i in issues if i.startswith("🔴")]) == 0,
        }


# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
checker = FreeATSChecker()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name="checkresume", description="Check your resume's ATS score")
@app_commands.describe(resume="Paste your resume text or attach a file")
async def check_resume(interaction: discord.Interaction, resume: str = None):
    """Analyze resume and return ATS score."""
    await interaction.response.defer()

    # Get text from attachment if no text provided
    if not resume and interaction.message.attachments:
        attachment = interaction.message.attachments[0]
        resume = await attachment.read()
        resume = resume.decode('utf-8', errors='ignore')

    if not resume:
        await interaction.followup.send(
            "Please paste your resume text or attach a file!",
            ephemeral=True
        )
        return

    # Run analysis
    result = checker.check(resume)

    # Format response
    score = result["score"]
    issues = result["issues"]

    if score >= 80:
        color = discord.Color.green()
        emoji = "✅"
    elif score >= 60:
        color = discord.Color.yellow()
        emoji = "⚠️"
    else:
        color = discord.Color.red()
        emoji = "❌"

    embed = discord.Embed(
        title=f"{emoji} ATS Score: {score}/100",
        description="Here's your resume analysis:",
        color=color,
    )

    if issues:
        embed.add_field(
            name="Issues Found",
            value="\n".join(issues[:5]),
            inline=False,
        )
    else:
        embed.add_field(
            name="No Major Issues",
            value="Your resume should pass most ATS systems!",
            inline=False,
        )

    embed.add_field(
        name="Want detailed analysis?",
        value="[Get full report on PlacementPro](https://placementpro.app/free-ats)",
        inline=False,
    )

    embed.set_footer(text="Powered by PlacementPro | Free ATS Checker")

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="score", description="Quick ATS score for text")
async def quick_score(interaction: discord.Interaction, text: str):
    """Quick score for any text."""
    result = checker.check(text)
    await interaction.response.send_message(
        f"**ATS Score: {result['score']}/100**\n"
        f"{'✅ Pass' if result['passed'] else '❌ Needs work'}",
        ephemeral=True
    )


@bot.tree.command(name="link", description="Get link to PlacementPro")
async def get_link(interaction: discord.Interaction):
    """Share the web app link."""
    embed = discord.Embed(
        title="PlacementPro - Free Interview Prep",
        description="AI-powered interview preparation platform",
        url="https://placementpro.app",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Free Features", value="• ATS Resume Checker\n• 3 Free Interviews\n• Basic Coding Challenges", inline=True)
    embed.add_field(name="Pro Features", value="• Unlimited Everything\n• Company-Specific Prep\n• Anti-Plagiarism Tailoring", inline=True)
    embed.set_footer(text="Start free at placementpro.app")

    await interaction.response.send_message(embed=embed)


# Run the bot
if __name__ == "__main__":
    import os
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Set DISCORD_BOT_TOKEN environment variable to run the bot")
