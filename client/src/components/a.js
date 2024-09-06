import {
    SignProtocolClient,
    SpMode,
    EvmChains,
    delegateSignAttestation,
    delegateSignRevokeAttestation,
    delegateSignSchema,
  } from "@ethsign/sp-sdk";
  import { privateKeyToAccount } from "viem/accounts";
  const privateKey = "0x2b45672b49ed7422d2cc12239c884fc9e7d4dc023a2f119c8873890c4771a49d"; // Optional
  
  const client = new SignProtocolClient(SpMode.OnChain, {
    chain: EvmChains.baseSepolia,
    account: privateKeyToAccount(privateKey), // Optional if you are using an injected provider
  });
  
  // Create schema
  // const createSchemaRes = await client.createSchema({
  //   name: "xxx",
  //   data: [{ name: "name", type: "string" }],
  // });
  // console.log("createSchemaRes", createSchemaRes);
//   // Create attestation
  const createAttestationRes = await client.createAttestation({
    schemaId: "0x3",
    data: { name: "a" },
    indexingValue: "xxx",
  });
  console.log(createAttestationRes)
  