// index.js
const axios = require('axios');

const run = async () => {
  const chatId = process.env.TELEGRAM_CHAT_ID;
  const botToken = process.env.TELEGRAM_BOT_TOKEN;

  if (!chatId || !botToken) {
    console.error("Missing environment variables");
    process.exit(1);
  }

  const res = await axios.post(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    chat_id: chatId,
    text: "Hello from Node.js Docker container!"
  });

  console.log("Message sent:", res.data);
};

run();
