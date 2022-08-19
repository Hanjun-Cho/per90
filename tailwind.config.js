module.exports = {
  content: ["./src/**/**/**.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        mont: ["MONT", "sans-serif"]
      }
    },
    colors: {
      'white':'#FFFFFF',
      'black':'#0d0d0d',
      'spurs-blue':'#132257',
      'blue':'#42a2d6'
    },
    screens: {
      'small':{'max':'860px'},
      'mini':{'max':'500px'}
    },
  },
  plugins: [],
}
