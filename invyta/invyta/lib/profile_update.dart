import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class SetUserProfile extends StatefulWidget {
  @override
  _SetUserProfileState createState() => _SetUserProfileState();
}

class _SetUserProfileState extends State<SetUserProfile> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _bioController = TextEditingController();
  final TextEditingController _favoriteController = TextEditingController();

  Map<String, dynamic>? _userData;
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    _fetchUserData();
  }

  // Fetch user data from the backend
  Future<void> _fetchUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final String? accessToken = prefs.getString('access_token');

    if (accessToken == null) {
      _showSnackBar('User not logged in');
      return;
    }

    try {
      final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/profile'), // Replace with your backend URL
        headers: {
          'Authorization': 'Bearer $accessToken',
        },
      );

      if (response.statusCode == 200) {
        setState(() {
          _userData = json.decode(response.body);
          _usernameController.text = _userData?['username'] ?? '';
          _bioController.text = _userData?['bio'] ?? '';
          _favoriteController.text = _userData?['favorite'] ?? '';
        });
      } else {
        _showSnackBar('Failed to fetch user data');
      }
    } catch (e) {
      _showSnackBar('An error occurred. Please try again.');
      print('Error: $e');
    }
  }

  // Update user data
  Future<void> _updateUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final String? accessToken = prefs.getString('access_token');

    if (accessToken == null) {
      _showSnackBar('User not logged in');
      return;
    }

    final Map<String, dynamic> requestBody = {
      'username': _usernameController.text.trim(),
      'bio': _bioController.text.trim(),
      'favorite': _favoriteController.text.trim(),
    };

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/profile'), // Replace with your backend URL
        headers: {
          'Authorization': 'Bearer $accessToken',
          'Content-Type': 'application/json',
        },
        body: json.encode(requestBody),
      );

      if (response.statusCode == 201) {
        _showSnackBar('Profile updated successfully!');
        setState(() {
          _isEditing = false;
        });
        _fetchUserData(); // Refresh user data
      } else {
        _showSnackBar('Failed to update profile');
      }
    } catch (e) {
      _showSnackBar('An error occurred. Please try again.');
      print('Error: $e');
    }
  }

  // Helper function to show a SnackBar
  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade400, Colors.purple.shade400],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: Card(
            elevation: 10,
            margin: EdgeInsets.all(20),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!_isEditing) ...[
                    Text(
                      'Username: ${_userData?['username'] ?? 'Not set'}',
                      style: TextStyle(fontSize: 18, color: Colors.blue.shade800),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Bio: ${_userData?['bio'] ?? 'Not set'}',
                      style: TextStyle(fontSize: 18, color: Colors.blue.shade800),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Favorite: ${_userData?['favorite'] ?? 'Not set'}',
                      style: TextStyle(fontSize: 18, color: Colors.blue.shade800),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Email: ${_userData?['email'] ?? 'Not set'}',
                      style: TextStyle(fontSize: 18, color: Colors.blue.shade800),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Joined: ${_userData?['created_on'] ?? 'Not set'}',
                      style: TextStyle(fontSize: 18, color: Colors.blue.shade800),
                    ),
                  ],
                  if (_isEditing) ...[
                    TextField(
                      controller: _usernameController,
                      decoration: InputDecoration(
                        labelText: 'Username',
                        labelStyle: TextStyle(color: Colors.blue.shade800),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Colors.blue.shade800),
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),),
                    SizedBox(height: 10),
                    TextField(
                      controller: _bioController,
                      decoration: InputDecoration(
                        labelText: 'Bio',
                        labelStyle: TextStyle(color: Colors.blue.shade800),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Colors.blue.shade800),
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),),
                    SizedBox(height: 10),
                    TextField(
                      controller: _favoriteController,
                      decoration: InputDecoration(
                        labelText: 'Favorite',
                        labelStyle: TextStyle(color: Colors.blue.shade800),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Colors.blue.shade800),
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),),
                    SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: _updateUserData,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue.shade800,
                        padding: EdgeInsets.symmetric(
                            horizontal: 40, vertical: 15),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      child: Text(
                        'Save',
                        style: TextStyle(fontSize: 16, color: Colors.white),
                      ),
                    ),
                  ],
                  SizedBox(height: 10),
                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton(
                      onPressed: () {
                        setState(() {
                          _isEditing = !_isEditing;
                        });
                      },
                      child: Text(
                        _isEditing ? 'Cancel' : 'Edit Profile',
                        style: TextStyle(color: Colors.blue.shade800),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}