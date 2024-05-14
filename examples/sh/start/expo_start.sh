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
mkdir src/components/buttons src/components/texts src/components/icons

npm i nativewind
npm i tailwindcss@3.3.2 --save-dev
npm i @react-navigation/native-stack
npx tailwind init


echo "import { Text } from \"react-native\";

function Paragraph(props: any) {
  return (
    <Text className=\"text-secondary text-justify text-lg mb-4\">
      {props.children}
    </Text>
  );
}

export { Paragraph };" > src/components/texts/Paragraph.tsx


echo "import { Text } from \"react-native\";

interface SubTitleProps {
  text: string;
  className?: string;
}

function SubTitle(props: SubTitleProps) {
  return (
    <Text className={\`text-2xl mb-5 text-primary \${props.className}\`}>
      {props.text}
    </Text>
  );
}

export { SubTitle };" > src/components/texts/SubTitle.tsx


echo "import { Text } from \"react-native\";

interface TitleProps {
  text: string;
  className?: string;
}

function Title(props: TitleProps) {
  return (
    <Text className={\`text-4xl mt-10 mb-5 text-primary \${props.className}\`}>
      {props.text}
    </Text>
  );
}

export { Title };" > src/components/texts/Title.tsx


echo "import { Feather } from \"@expo/vector-icons\";
import colors from \"tailwindcss/colors\";

interface IconProps {
  name: keyof typeof Feather.glyphMap;
  size?: number;
}

function Icon(props: IconProps) {
  return (
    <Feather
      name={props.name}
      size={props.size ? props.size : 50}
      color={colors.blue[500]}
    />
  );
}

export { Icon };" > src/components/icons/Icon.tsx


echo "import { TouchableOpacity, Text, GestureResponderEvent } from \"react-native\";

interface TertiaryButtonProps {
  text: string;
  btnClassName?: string;
  textClassName?: string;
  onPress?: (event: GestureResponderEvent) => void;
}

function TertiaryButton(props: TertiaryButtonProps) {
  return (
    <TouchableOpacity
      className={\`border-2 my-2 mx-5 border-transparent rounded-xl \${props.btnClassName}\`}
      onPress={props.onPress}
    >
      <Text
        className={\`text-xl text-center text-secondary py-2 px-5 \${props.textClassName}\`}
      >
        {props.text}
      </Text>
    </TouchableOpacity>
  );
}

export { TertiaryButton };" > src/components/buttons/TertiaryButton.tsx


echo "import { TouchableOpacity, Text, GestureResponderEvent } from \"react-native\";

interface SecondaryButtonProps {
  text: string;
  btnClassName?: string;
  textClassName?: string;
  onPress?: (event: GestureResponderEvent) => void;
}

function SecondaryButton(props: SecondaryButtonProps) {
  return (
    <TouchableOpacity
      className={\`border-2 border-solid border-secondary my-2 mx-5 rounded-xl \${props.btnClassName}\`}
      onPress={props.onPress}
    >
      <Text
        className={\`text-xl text-center text-secondary py-2 px-5 \${props.textClassName}\`}
      >
        {props.text}
      </Text>
    </TouchableOpacity>
  );
}

export { SecondaryButton };" > src/components/buttons/SecondaryButton.tsx


echo "import { TouchableOpacity, Text, GestureResponderEvent } from \"react-native\";

interface PrimaryButtonProps {
  text: string;
  btnClassName?: string;
  textClassName?: string;
  onPress?: (event: GestureResponderEvent) => void;
}

function PrimaryButton(props: PrimaryButtonProps) {
  return (
    <TouchableOpacity
      className={\`border-2 border-solid border-primary bg-primary rounded-xl my-2 mx-5 \${props.btnClassName}\`}
      onPress={props.onPress}
    >
      <Text
        className={\`text-xl text-center text-baseColor py-2 px-5 \${props.textClassName}\`}
      >
        {props.text}
      </Text>
    </TouchableOpacity>
  );
}

export { PrimaryButton };" > src/components/buttons/PrimaryButton.tsx


echo "import { SafeAreaView, ScrollView } from \"react-native\";

import { Title } from \"../components/texts/Title\";
import { SubTitle } from \"../components/texts/SubTitle\";
import { PrimaryButton } from \"../components/buttons/PrimaryButton\";
import { SecondaryButton } from \"../components/buttons/SecondaryButton\";
import { TertiaryButton } from \"../components/buttons/TertiaryButton\";
import { Icon } from \"../components/icons/Icon\";
import { Paragraph } from \"../components/texts/Paragraph\";

export function Home({ navigation }: { navigation: any }) {
  return (
    <SafeAreaView className=\"bg-baseColor px-10 py-5 h-full w-full\">
      <ScrollView showsVerticalScrollIndicator={false}>
        <Title text=\"Title\" />
        <SubTitle text=\"Subtitle\" />
        <PrimaryButton
          text=\"Primary Btn\"
          onPress={() => navigation.navigate(\"Details\")}
        />
        <SecondaryButton text=\"Secondary Btn\" />
        <TertiaryButton text=\"Tertiary Btn\"/>
        <Icon name=\"home\" />
        <Paragraph>
          Donec mollis ante dictum dapibus gravida. Pellentesque commodo dolor
          vel ante molestie, ac lacinia diam ullamcorper. Phasellus ante urna,
          lobortis sit amet cursus in, consequat non libero. Nam accumsan mauris
          sed consectetur sodales. Cras erat quam, rutrum ultrices tempor a,
          efficitur eget metus.
        </Paragraph>
      </ScrollView>
    </SafeAreaView>
  );
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

echo "import * as React from \"react\";
import { NavigationContainer } from \"@react-navigation/native\";
import { createNativeStackNavigator } from \"@react-navigation/native-stack\";
import { StatusBar } from \"expo-status-bar\";
import colors from \"tailwindcss/colors\";

import { Home } from \"./src/screens/Home\";
import { Details } from \"./src/screens/Details\";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style=\"dark\" backgroundColor={colors.blue[200]} />
      <Stack.Navigator screenOptions={{ headerTransparent: true, title: \"\" }}>
        <Stack.Screen name=\"Home\" component={Home} />
        <Stack.Screen name=\"Details\" component={Details} />
        {/* Other screens here */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}" > App.tsx

echo "/// <reference types=\"nativewind/types\" />" > app.d.ts

echo "/** @type {import('tailwindcss').Config} */

const colors = require(\"tailwindcss/colors\");

module.exports = {
  content: [\"./App.tsx\", \"./src/**/*.tsx\"],
  theme: {
    extend: {
      colors: {
        baseColor: colors.blue[200],
        primary: colors.blue[700],
        secondary: colors.blue[500],
      },
    },
  },
  plugins: [],
};
" > tailwind.config.js

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
