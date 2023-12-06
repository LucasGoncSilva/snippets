echo "
 ____  _  _  ____   __        ____  ____  __   ____  ____    ____  _  _ 
(  __)( \/ )(  _ \ /  \      / ___)(_  _)/ _\ (  _ \(_  _)  / ___)/ )( \\
 ) _)  )  (  ) __/(  O )____ \___ \  )( /    \ )   /  )(  _ \___ \) __ (
(____)(_/\_)(__)   \__/(____)(____/ (__)\_/\_/(__\_) (__)(_)(____/\_)(_/
"

printf "Write your app's name: "
read APP_NAME

npx create-expo-app $APP_NAME -t expo-template-blank-typescript

cd $APP_NAME

mkdir src src/screens src/components

npm i nativewind
npm i tailwindcss@3.3.2 --save-dev
npm i @react-navigation/native-stack
npx tailwind init

echo "import { View, Text, Button } from 'react-native';

export function Home({ navigation }: { navigation: any }) {
  return (
    <View className=\"flex-1 justify-center items-center\" >
      <Text>Home</Text>
      <Button
        title=\"Go to Details\"
        onPress={() => navigation.navigate('Details')}
      />
    </View>
  )
}" > src/screens/Home.tsx

echo "import { View, Text, Button } from 'react-native';

export function Details({ navigation }: { navigation: any }) {
  return (
    <View className=\"flex-1 justify-center items-center\" >
      <Text>Details</Text>
      <Button
        title=\"Go to Home\"
        onPress={() => navigation.navigate('Home')}
      />
    </View>
  )
}" > src/screens/Details.tsx

echo "import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { Home } from './src/screens/Home';
import { Details } from './src/screens/Details';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerTransparent: true, title: '' }}>
        <Stack.Screen name=\"Home\" component={Home} />
        <Stack.Screen name=\"Details\" component={Details} />
        {/* Other screens here */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}" > App.tsx

echo "/// <reference types=\"nativewind/types\" />" > app.d.ts

echo "/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    \"./App.tsx\",
    \"./src/**/*.tsx\"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}" > tailwind.config.js

echo "module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ['nativewind/babel'],
  };
};" > babel.config.js

git add .
git commit -m "automated task done"

npm run start
