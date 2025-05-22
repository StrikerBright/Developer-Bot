import discord
from discord.ui import View, Select, Modal, TextInput

TICKET_CHANNEL_ID = 1374871127796486226      # Channel to send the ticket embed
TICKET_CATEGORY_ID = 1374972990307041301     # Category for ticket channels
TRANSCRIPT_CHANNEL_ID = 1374973012608024596  # Channel for transcripts (not used here)

# --- Modal for ticket details ---
class InquiryModal(Modal):
    def __init__(self, inquiry_type: str):
        super().__init__(title=f"{inquiry_type} Ticket")
        self.inquiry_type = inquiry_type
        self.add_item(TextInput(label="Describe your issue", placeholder="Please provide details..."))

    async def callback(self, interaction: discord.Interaction):
        reason = self.children[0].value
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY_ID)
        # Debug print for troubleshooting
        print(f"[DEBUG] Category: {category} (ID: {TICKET_CATEGORY_ID})")
        if category is None or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "Ticket category not found or is not a category. Please contact an admin.",
                ephemeral=True
            )
            return
        # Permissions for the new ticket channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        # Format channel name: username-inquirytype (lowercase, spaces to dashes)
        safe_inquiry = self.inquiry_type.lower().replace(" ", "-")
        safe_username = interaction.user.name.lower().replace(" ", "-")
        channel_name = f"{safe_username}-{safe_inquiry}"
        # Create the ticket channel
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"{self.inquiry_type} ticket for {interaction.user}"
        )
        await ticket_channel.send(
            f"{interaction.user.mention} created a **{self.inquiry_type}** ticket.\n**Reason:** {reason}"
        )
        await interaction.response.send_message(
            f"Your ticket has been created: {ticket_channel.mention}", ephemeral=True
        )

# --- Dropdown for inquiry types ---
class InquirySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Commissioning help", description="Get help with commissioning issues"),
            discord.SelectOption(label="Enlisting help", description="Get help with enlisting issues"),
            discord.SelectOption(label="Other", description="Other inquiries"),
        ]
        super().__init__(placeholder="Choose your inquiry type...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        inquiry_type = self.values[0]
        await interaction.response.send_modal(InquiryModal(inquiry_type))

# --- View for the dropdown ---
class InquiryView(View):
    def __init__(self):
        super().__init__()
        self.add_item(InquirySelect())

# --- Function to send the ticket embed with dropdown ---
async def send_ticket_embed(bot):
    channel = bot.get_channel(TICKET_CHANNEL_ID)
    # Prevent duplicate embeds by checking for a previous bot message
    async for msg in channel.history(limit=10):
        if msg.author == bot.user and msg.components:
            return  # Already sent
    embed = discord.Embed(
        title="Speak with a DCNG recruiter",
        description="If you have any questions or need assistance, please select an inquiry type from the dropdown below.",
        color=discord.Color.greyple()
    )
    await channel.send(embed=embed, view=InquiryView())