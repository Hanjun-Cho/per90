module.exports = {
  content: ["./src/**/**/**.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        mont: ["MONT", "sans-serif"],
        modern_sans: ["MODERN_SANS", "sans-serif"],
        gravity: ["GRAVITY", "sans-serif"],
        gravity_bold: ["GRAVITY_BOLD", "sans-serif"],
        roboto: ["ROBOTO", "sans-serif"]
      }
    },
    colors: {
      'white':'#FFFFFF',
      'red':'#de4e4e',
      'black':'#0d0d0d',
      'lighter-black':'#101010',
      'spurs-blue':'#132257',
      'blue':'#42a2d6',
      "yellow":"e0ec5f",
      "dark-yellow":"#B4BF40"
    },
    screens: {
      'large':{'min':'861px'},
      'small':{'max':'860px'},
      'mini':{'max':'500px'}
    },
  },
  plugins: [],
}
