/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2022: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    // Vue相关规则
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',

    // TypeScript相关规则
    '@typescript-eslint/no-unused-vars': [
      'warn',
      {
        argsIgnorePattern: '^_',
        varsIgnorePattern:
          '^_|^(props|emit|features|loadChapters|results|deleteChat|speechRecognizer|handleSessionSelect|handleCreateSession|isKnowledgePage|goToKnowledge|sendSMS|watch|Plus|levels|Refresh|DataAnalysis|Document|ArrowLeft|AITriageResponse|SessionManager)$',
        ignoreRestSiblings: true,
      },
    ],
    '@typescript-eslint/no-explicit-any': 'off', // 演示项目中允许使用any

    // 通用规则
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
  },
  overrides: [
    {
      files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
      env: {
        jest: true,
      },
    },
    {
      files: ['e2e/**/*.{test,spec}.{js,ts,jsx,tsx}'],
      env: {
        node: true,
      },
    },
  ],
  ignorePatterns: ['dist', 'node_modules', '*.d.ts', 'auto-imports.d.ts', 'components.d.ts'],
}
