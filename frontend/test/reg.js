function generateRandomString(length = 10) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

const test_sample="js"
const matchJS = /js$/

function testSampleStringPatternTime(){
    let strings = []
    for (let i = 0; i < 1000000; i++) {
        const string = generateRandomString(100)
        strings.push(string)
    }
    const start = new Date().getTime()
    strings.forEach(string => {
        const index= string.endsWith(test_sample)
    })
    const end = new Date().getTime()
    console.log(`String.prototype.endsWith: ${end - start}ms`)
}

function testRegStringPatternTime(){
    let strings = []
    for (let i = 0; i < 1000000; i++) {
        const string = generateRandomString(100)
        strings.push(string)
    }
    const start = new Date().getTime()
    strings.forEach(string => {
        matchJS.test(string)
    })
    const end = new Date().getTime()
    console.log(`reg_test: ${end - start}ms`)
}

testSampleStringPatternTime()
testRegStringPatternTime()