const axios = require("axios");

async function main() {

    const resposta =
        await axios.get(
            "http://localhost:5000/animais"
        );

    console.log(resposta.data);
}

main();
