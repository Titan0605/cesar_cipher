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
const REGISTER_REGEX = /^!register\s+(\S+)$/i;
const LOGIN_REGEX = /^!login\s+(\S+)$/i;
const FLASK_API_URL = "http://127.0.0.1:5000/api";

const activeSessions = new Set();

async function callCipherAPI(endpoint, text, shift) {
  const response = await fetch(`${FLASK_API_URL}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, shift: parseInt(shift) }),
  });
  const data = await response.json();
  return data.result;
}

async function callAuthAPI(endpoint, username, password) {
  const response = await fetch(`${FLASK_API_URL}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return { status: response.status, data: await response.json() };
}

function isAuthenticated(phone) {
  return activeSessions.has(phone);
}

client.on("message", async (message) => {
  if(message.fromMe) return
  const chat = await message.getChat();
  const contact = await message.getContact();
  const phone = contact.number;

  if (REGISTER_REGEX.test(message.body)) {
    const [, password] = message.body.match(REGISTER_REGEX);
    try {
      const { status } = await callAuthAPI("register", phone, password);
      if (status === 201) {
        await message.reply("✅ Registrado exitosamente.");
      } else if (status === 409) {
        await message.reply("⚠️ Ya estás registrado.");
      } else {
        await message.reply("❌ Error al registrar.");
      }
    } catch (err) {
      console.error("Error calling register API:", err);
      await message.reply("❌ Error al registrar.");
    }
  } else if (LOGIN_REGEX.test(message.body)) {
    const [, password] = message.body.match(LOGIN_REGEX);
    try {
      const { status } = await callAuthAPI("login", phone, password);
      if (status === 200) {
        activeSessions.add(phone);
        await message.reply("✅ Bienvenido! Ya puedes usar los comandos.");
      } else if (status === 404) {
        await message.reply("❌ Usuario no encontrado. Usa !register <contraseña> primero.");
      } else if (status === 401) {
        await message.reply("❌ Contraseña incorrecta.");
      } else {
        await message.reply("❌ Error al iniciar sesión.");
      }
    } catch (err) {
      console.error("Error calling login API:", err);
      await message.reply("❌ Error al iniciar sesión.");
    }
  } else if (message.body.toLowerCase() === "ping") {
    if (!isAuthenticated(phone)) {
      await message.reply("❌ Debes hacer !login primero.");
      return;
    }
    await message.reply("pong");
  } else if (CYPHER_REGEX.test(message.body)) {
    if (!isAuthenticated(phone)) {
      await message.reply("❌ Debes hacer !login primero.");
      return;
    }
    const [, word, shift] = message.body.match(CYPHER_REGEX);
    try {
      const result = await callCipherAPI("encrypt", word, shift);
      await message.reply(result);
    } catch (err) {
      console.error("Error calling encrypt API:", err);
      await message.reply("Error al encriptar el mensaje.");
    }
  } else if (DECYPHER_REGEX.test(message.body)) {
    if (!isAuthenticated(phone)) {
      await message.reply("❌ Debes hacer !login primero.");
      return;
    }
    const [, word, shift] = message.body.match(DECYPHER_REGEX);
    try {
      const result = await callCipherAPI("decrypt", word, shift);
      await message.reply(result);
    } catch (err) {
      console.error("Error calling decrypt API:", err);
      await message.reply("Error al desencriptar el mensaje.");
    }
  } else if (message.body.toLowerCase() === "que") {
    if (!isAuthenticated(phone)) {
      await message.reply("❌ Debes hacer !login primero.");
      return;
    }
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
