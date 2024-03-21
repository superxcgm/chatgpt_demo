const express = require('express');
const app = express();
const fs = require('fs');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// Middleware to parse request bodies
app.use(bodyParser.json());

// Load users from file
function loadUsersFromFile() {
    try {
        const usersData = fs.readFileSync('users.json');
        return JSON.parse(usersData);
    } catch (error) {
        return [];
    }
}

// Save users to file
function saveUsersToFile(users) {
    fs.writeFileSync('users.json', JSON.stringify(users, null, 2));
}

app.post('/signup', (req, res) => {
    const { username, password } = req.body;

    // Validate username
    const usernameRegex = /^[a-z]+$/;
    if (!username || !usernameRegex.test(username) || username.length < 8 || username.length > 20) {
        return res.status(400).json({ error: 'Invalid username. It should contain lowercase letters only and have a length of 8 to 20 characters.' });
    }

    // Validate password
    if (!password || password.length < 8) {
        return res.status(400).json({ error: 'Invalid password. It should have a minimum length of 8 characters.' });
    }

    const users = loadUsersFromFile();

    // Check if username already exists
    if (users.find((user) => user.username === username)) {
        return res.status(400).json({ error: 'Username already exists.' });
    }

    // Encrypt password
    const hashedPassword = bcrypt.hashSync(password, 10);

    // Save user to file
    users.push({ username, password: hashedPassword });
    saveUsersToFile(users);

    res.json({ message: 'Signup successful' });
});

// Login
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    const users = loadUsersFromFile();

    // Find user by username
    const user = users.find((user) => user.username === username);

    // Check if user exists and password is correct
    if (!user || !bcrypt.compareSync(password, user.password)) {
        return res.status(401).json({ error: 'Invalid username or password' });
    }

    // Generate JWT token
    const token = jwt.sign({ username }, 'secretKey');

    res.json({ message: 'Login successful', token });
});

// Middleware to protect routes
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Access token not found' });
    }

    jwt.verify(token, 'secretKey', (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
    });
}

// GET /meetups - Get all meetups
app.get('/meetups', (req, res) => {
    const meetups = readMeetupsFromFile();
    res.json(meetups);
});

app.use(authenticateToken);

app.post('/meetups', (req, res) => {
    const meetup = {
        id: generateUniqueId(),
        title: req.body.title,
        summary: req.body.summary,
        address: req.body.address
    };

    // Check if all required fields are present
    if (!meetup.id || !meetup.title || !meetup.summary || !meetup.address) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const meetups = readMeetupsFromFile();
    meetups.push(meetup);
    writeMeetupsToFile(meetups);

    res.status(201).json({ message: 'Meetup created successfully', id: meetup.id });
});

// Helper function to generate a unique ID
function generateUniqueId() {
    const { v4: uuidv4 } = require('uuid');
    return uuidv4();
}

// Helper function to read meetups from the JSON file
function readMeetupsFromFile() {
    const meetupsData = fs.readFileSync('meetups.json');
    return JSON.parse(meetupsData);
}

// Helper function to write meetups to the JSON file
function writeMeetupsToFile(meetups) {
    const meetupsData = JSON.stringify(meetups, null, 2);
    fs.writeFileSync('meetups.json', meetupsData);
}

app.patch('/meetups/:id', (req, res) => {
    const id = req.params.id;
    const updatedMeetup = {
        title: req.body.title,
        summary: req.body.summary,
        address: req.body.address
    };

    if (!updatedMeetup.title && !updatedMeetup.summary && !updatedMeetup.address) {
        return res.status(400).json({ error: 'No fields to update' });
    }

    const meetups = readMeetupsFromFile();
    const meetupIndex = meetups.findIndex((meetup) => meetup.id === id);

    if (meetupIndex === -1) {
        return res.status(404).json({ error: 'Meetup not found' });
    }

    const originalMeetup = meetups[meetupIndex];
    console.log('originMeetup', JSON.stringify(originalMeetup));
    console.log('updatedMeetup', JSON.stringify(updatedMeetup));
    const updatedMeetupData = Object.assign({}, originalMeetup, removeEmptyFields(updatedMeetup));
    console.log('updatedMeetupData', JSON.stringify(updatedMeetupData));
    meetups[meetupIndex] = updatedMeetupData;
    writeMeetupsToFile(meetups);

    res.json({ message: 'Meetup updated successfully' });
});

function removeEmptyFields(obj) {
    // Create a new object to store the result
    const result = {};

    // Iterate over the object's properties
    for (const [key, value] of Object.entries(obj)) {
        // Check if the value is not empty
        if (value !== null && value !== undefined && value !== '') {
            // Add the non-empty field to the result object
            result[key] = value;
        }
    }

    return result;
}

// DELETE /meetups/:id - Delete a meetup
app.delete('/meetups/:id', (req, res) => {
    const id = req.params.id;
    const meetups = readMeetupsFromFile();

    // Filter out the meetup with the given id from the meetups array
    new_meetups = meetups.filter((meetup) => meetup.id !== id);
    writeMeetupsToFile(new_meetups);

    res.json({ message: 'Meetup deleted successfully' });
});

// Start the server
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});