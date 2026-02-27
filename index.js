const { Client, LocalAuth, MessageMedia, MessageAck } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const client = new Client({
  authStrategy: new LocalAuth(),
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("Client is ready!");
});

const CYPHER_REGEX = /^!cypher\s+(.+)\s+(\d+)$/i;
const DECYPHER_REGEX = /^!decypher\s+(.+)\s+(\d+)$/i;
const FLASK_API_URL = "http://127.0.0.1:5000/api";

async function callCipherAPI(endpoint, text, shift) {
  const response = await fetch(`${FLASK_API_URL}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, shift: parseInt(shift) }),
  });
  const data = await response.json();
  return data.result;
}

client.on("message", async (message) => {
  const chat = await message.getChat();

  if (message.body.toLowerCase() === "ping") {
    await message.reply("pong");

  } else if (CYPHER_REGEX.test(message.body)) {
    const [, word, shift] = message.body.match(CYPHER_REGEX);
    try {
      const result = await callCipherAPI("encrypt", word, shift);
      await message.reply(result);
    } catch (err) {
      console.error("Error calling encrypt API:", err);
      await message.reply("Error al encriptar el mensaje.");
    }

  } else if (DECYPHER_REGEX.test(message.body)) {
    const [, word, shift] = message.body.match(DECYPHER_REGEX);
    try {
      const result = await callCipherAPI("decrypt", word, shift);
      await message.reply(result);
    } catch (err) {
      console.error("Error calling decrypt API:", err);
      await message.reply("Error al desencriptar el mensaje.");
    }

  } else if (message.body.toLowerCase() === "que") {
    const url = "https://images7.memedroid.com/images/UPLOADED574/625f4dd6290b4.jpeg";

    try {
      const media = await MessageMedia.fromUrl(url);
      await client.sendMessage(message.from, media, {
        sendMediaAsSticker: true,
        stickerAuthor: "MyBot",
        stickerName: "Sticker",
      });
    } catch (err) {
      console.error("Failed to send sticker: ", err);
    }
  }
});

client.initialize();
