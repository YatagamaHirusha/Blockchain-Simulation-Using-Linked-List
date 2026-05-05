const { Blockchain, Transaction } = require('./blockchain');
const EC = require('elliptic').ec;
const ec = new EC('secp256k1');

const myKery = ec.keyFromPrivate('5f19af638ea3e994e1aa407e61114f81288c9a8be4105a8ba1e37bf88ef58f8a');
const myWalletAddress = myKery.getPublic('hex');

let transactionCoin = new Blockchain();

const tx1 = new Transaction(myWalletAddress, 'receiver-address/key', 10);
tx1.signTransaction(myKery);
transactionCoin.creatTransaction(tx1);

console.log("\n Starting the miner...");
transactionCoin.minePendingTransactions(myWalletAddress);

console.log("\nBalance of xavier is", transactionCoin.getBalanceOfAddress(myWalletAddress));
console.log("\nis chain valid?", transactionCoin.isChainValid());